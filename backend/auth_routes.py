"""
Authentication and User Management Routes
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from typing import Optional
from .models import User, UserSession, SavedVideo, Export, get_db
from .auth import (
    hash_password, verify_password, create_access_token, 
    decode_token, generate_unique_id
)
from .utils.language_support import validate_language_code, SUPPORTED_LANGUAGES
import json

router = APIRouter(prefix="/auth", tags=["authentication"])

# Pydantic Models
class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    user_id: str
    username: str
    email: str
    preferred_language: str


class UserPreferencesUpdate(BaseModel):
    full_name: Optional[str] = None
    preferred_language: Optional[str] = None


class SaveVideoRequest(BaseModel):
    video_id: str
    title: str
    source: str  # 'youtube', 'podcast', 'spotify', 'local'
    url: str
    thumbnail: Optional[str] = None


class ExportRequest(BaseModel):
    video_id: str
    export_type: str  # 'notion', 'google_doc', 'markdown', 'docx'
    export_url: Optional[str] = None


def _get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """Dependency to get current authenticated user"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    try:
        # Extract token from "Bearer <token>"
        parts = authorization.split()
        if len(parts) != 2 or parts[0] != "Bearer":
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        token = parts[1]
        payload = decode_token(token)
        
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_id = payload.get("user_id")
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="User not found or inactive")
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")


@router.post("/signup", response_model=AuthResponse)
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """Create a new user account"""
    try:
        # Check if user exists
        existing_user = db.query(User).filter(
            (User.email == request.email) | (User.username == request.username)
        ).first()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Create new user
        user_id = generate_unique_id()
        user = User(
            id=user_id,
            username=request.username,
            email=request.email,
            full_name=request.full_name,
            hashed_password=hash_password(request.password),
            preferred_language="en"
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Generate token
        token = create_access_token({"user_id": user_id, "email": request.email})
        
        return AuthResponse(
            access_token=token,
            user_id=user_id,
            username=user.username,
            email=user.email,
            preferred_language=user.preferred_language
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")


@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return token"""
    try:
        user = db.query(User).filter(User.email == request.email).first()
        
        if not user or not verify_password(request.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not user.is_active:
            raise HTTPException(status_code=403, detail="User account is inactive")
        
        # Generate token
        token = create_access_token({"user_id": user.id, "email": user.email})
        
        return AuthResponse(
            access_token=token,
            user_id=user.id,
            username=user.username,
            email=user.email,
            preferred_language=user.preferred_language
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.get("/me")
def get_current_user_info(
    current_user: User = Depends(_get_current_user)
):
    """Get current user information"""
    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "preferred_language": current_user.preferred_language,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at.isoformat()
    }


@router.put("/preferences")
def update_user_preferences(
    request: UserPreferencesUpdate,
    current_user: User = Depends(_get_current_user),
    db: Session = Depends(get_db)
):
    """Update user preferences including language"""
    try:
        if request.full_name:
            current_user.full_name = request.full_name
        
        if request.preferred_language:
            if not validate_language_code(request.preferred_language):
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported language. Supported: {', '.join(SUPPORTED_LANGUAGES.keys())}"
                )
            current_user.preferred_language = request.preferred_language
        
        db.commit()
        db.refresh(current_user)
        
        return {
            "message": "Preferences updated successfully",
            "preferred_language": current_user.preferred_language,
            "full_name": current_user.full_name
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")


@router.post("/change-password")
def change_password(
    old_password: str,
    new_password: str,
    current_user: User = Depends(_get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    try:
        if not verify_password(old_password, current_user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid current password")
        
        if len(new_password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
        
        current_user.hashed_password = hash_password(new_password)
        db.commit()
        
        return {"message": "Password changed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Password change failed: {str(e)}")


@router.post("/save-video")
def save_video(
    request: SaveVideoRequest,
    current_user: User = Depends(_get_current_user),
    db: Session = Depends(get_db)
):
    """Save a video to user's library"""
    try:
        saved_video = SavedVideo(
            id=generate_unique_id(),
            user_id=current_user.id,
            video_id=request.video_id,
            title=request.title,
            source=request.source,
            url=request.url,
            thumbnail=request.thumbnail
        )
        
        db.add(saved_video)
        db.commit()
        
        return {
            "message": "Video saved successfully",
            "saved_video_id": saved_video.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Save video failed: {str(e)}")


@router.get("/saved-videos")
def get_saved_videos(
    current_user: User = Depends(_get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's saved videos"""
    try:
        videos = db.query(SavedVideo).filter(
            SavedVideo.user_id == current_user.id
        ).order_by(SavedVideo.saved_at.desc()).all()
        
        return {
            "count": len(videos),
            "videos": [
                {
                    "id": v.id,
                    "video_id": v.video_id,
                    "title": v.title,
                    "source": v.source,
                    "url": v.url,
                    "thumbnail": v.thumbnail,
                    "saved_at": v.saved_at.isoformat()
                }
                for v in videos
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get saved videos: {str(e)}")


@router.delete("/saved-videos/{saved_video_id}")
def delete_saved_video(
    saved_video_id: str,
    current_user: User = Depends(_get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a saved video"""
    try:
        video = db.query(SavedVideo).filter(
            (SavedVideo.id == saved_video_id) & (SavedVideo.user_id == current_user.id)
        ).first()
        
        if not video:
            raise HTTPException(status_code=404, detail="Saved video not found")
        
        db.delete(video)
        db.commit()
        
        return {"message": "Saved video deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")


@router.post("/save-export")
def save_export(
    request: ExportRequest,
    current_user: User = Depends(_get_current_user),
    db: Session = Depends(get_db)
):
    """Track an export to external platform"""
    try:
        export = Export(
            id=generate_unique_id(),
            user_id=current_user.id,
            video_id=request.video_id,
            export_type=request.export_type,
            export_url=request.export_url or ""
        )
        
        db.add(export)
        db.commit()
        
        return {
            "message": "Export tracked successfully",
            "export_id": export.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Save export failed: {str(e)}")


@router.get("/exports")
def get_user_exports(
    current_user: User = Depends(_get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's exports"""
    try:
        exports = db.query(Export).filter(
            Export.user_id == current_user.id
        ).order_by(Export.created_at.desc()).all()
        
        return {
            "count": len(exports),
            "exports": [
                {
                    "id": e.id,
                    "video_id": e.video_id,
                    "export_type": e.export_type,
                    "export_url": e.export_url,
                    "created_at": e.created_at.isoformat()
                }
                for e in exports
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get exports: {str(e)}")
