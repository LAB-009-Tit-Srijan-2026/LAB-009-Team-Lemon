"""
Routes for advanced features: Spotify, Podcasts, Exports, Multi-language
"""
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
import asyncio
from .models import User, get_db
from .auth_routes import _get_current_user
from .utils.streaming_platform import (
    ingest_spotify_episode, ingest_podcast_episode, parse_streaming_url
)
from .utils.export_handler import export_content
from .utils.language_support import translate_content, SUPPORTED_LANGUAGES
from .session import add_to_session, get_session_history
import uuid

router = APIRouter(prefix="/features", tags=["features"])


class ExportSummaryRequest(BaseModel):
    video_id: str
    video_title: str
    export_type: str  # 'notion', 'docx', 'markdown', 'google_docs'
    include_qa_history: bool = False


class TranslateTextRequest(BaseModel):
    text: str
    target_language: str


class IngestStreamingRequest(BaseModel):
    url: str
    title: Optional[str] = None


@router.post("/export/summary")
async def export_summary(
    request: ExportSummaryRequest,
    current_user: User = Depends(_get_current_user),
    db: Session = Depends(get_db)
):
    """Export video summary to external platform"""
    try:
        from .summarizer import get_summary, get_topic_summaries
        from .session import get_session_history
        
        # Get summary and topics
        summary_text = get_summary(request.video_id)
        topics = get_topic_summaries(request.video_id)
        
        # Get Q&A history if requested
        qa_history = None
        if request.include_qa_history:
            # This would need a session_id to work properly
            # For now, we'll just export summary and topics
            pass
        
        # Export based on type
        result = await export_content(
            export_type=request.export_type,
            video_title=request.video_title,
            summary=summary_text,
            topics=topics,
            video_id=request.video_id,
            conversation_history=qa_history
        )
        
        if not result:
            raise HTTPException(
                status_code=400,
                detail=f"Export type '{request.export_type}' not supported or not configured"
            )
        
        # For docx, return file bytes; for others return URL or text
        if request.export_type == "docx":
            return {
                "message": "Export prepared",
                "type": "binary",
                "data": result.hex() if isinstance(result, bytes) else result
            }
        elif request.export_type == "markdown":
            return {
                "message": "Export successful",
                "type": "text",
                "content": result
            }
        else:
            # For Notion, Google Docs, etc.
            return {
                "message": "Export successful",
                "type": "url",
                "url": result
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@router.post("/ingest/spotify")
async def ingest_spotify(
    request: IngestStreamingRequest,
    current_user: User = Depends(_get_current_user),
    db: Session = Depends(get_db)
):
    """Ingest a Spotify episode"""
    try:
        job_id = str(uuid.uuid4())
        video_id = str(uuid.uuid4())
        
        # Run in background
        loop = asyncio.get_event_loop()
        loop.create_task(_ingest_spotify_background(job_id, video_id, request.url))
        
        return {
            "job_id": job_id,
            "video_id": video_id,
            "status": "processing",
            "message": "Spotify episode ingestion started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Spotify ingest failed: {str(e)}")


@router.post("/ingest/podcast")
async def ingest_podcast(
    request: IngestStreamingRequest,
    current_user: User = Depends(_get_current_user),
    db: Session = Depends(get_db)
):
    """Ingest a podcast episode from RSS feed or direct URL"""
    try:
        job_id = str(uuid.uuid4())
        video_id = str(uuid.uuid4())
        
        # Run in background
        loop = asyncio.get_event_loop()
        loop.create_task(_ingest_podcast_background(job_id, video_id, request.url))
        
        return {
            "job_id": job_id,
            "video_id": video_id,
            "status": "processing",
            "message": "Podcast episode ingestion started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Podcast ingest failed: {str(e)}")


@router.post("/ingest/auto")
async def ingest_auto(
    request: IngestStreamingRequest,
    current_user: User = Depends(_get_current_user),
    db: Session = Depends(get_db)
):
    """Automatically detect and ingest from any supported platform"""
    try:
        platform = parse_streaming_url(request.url)
        
        if platform == "spotify":
            return await ingest_spotify(request, current_user, db)
        elif platform == "podcast":
            return await ingest_podcast(request, current_user, db)
        elif platform == "youtube":
            # Use existing YouTube ingest endpoint
            raise HTTPException(
                status_code=400,
                detail="Use /ingest endpoint for YouTube videos"
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="URL not recognized. Supported: Spotify, Podcasts, YouTube"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Auto ingest failed: {str(e)}")


@router.post("/translate")
async def translate_text(
    request: TranslateTextRequest,
    current_user: User = Depends(_get_current_user)
):
    """Translate text to specified language"""
    try:
        if request.target_language not in SUPPORTED_LANGUAGES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language. Supported: {', '.join(SUPPORTED_LANGUAGES.keys())}"
            )
        
        translated = await translate_content(request.text, request.target_language)
        
        return {
            "original": request.text,
            "translated": translated,
            "language": request.target_language,
            "language_name": SUPPORTED_LANGUAGES[request.target_language]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@router.get("/languages")
def get_supported_languages():
    """Get list of supported languages for translation"""
    return {
        "languages": [
            {"code": code, "name": name}
            for code, name in SUPPORTED_LANGUAGES.items()
        ],
        "count": len(SUPPORTED_LANGUAGES)
    }


# Background tasks
async def _ingest_spotify_background(job_id: str, video_id: str, url: str):
    """Background task to ingest Spotify episode"""
    try:
        transcript = await ingest_spotify_episode(url, video_id)
        if transcript:
            print(f"Spotify ingest completed: {job_id}")
        else:
            print(f"Spotify ingest failed: {job_id} - No transcript generated")
    except Exception as e:
        print(f"Spotify ingest error: {job_id} - {str(e)}")


async def _ingest_podcast_background(job_id: str, video_id: str, url: str):
    """Background task to ingest podcast episode"""
    try:
        transcript = await ingest_podcast_episode(url, video_id)
        if transcript:
            print(f"Podcast ingest completed: {job_id}")
        else:
            print(f"Podcast ingest failed: {job_id} - No transcript generated")
    except Exception as e:
        print(f"Podcast ingest error: {job_id} - {str(e)}")
