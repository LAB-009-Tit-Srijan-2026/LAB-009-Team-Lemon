"""
Spotify and Podcast support for Alexandria
"""
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import requests
from typing import Optional, Dict, List
import asyncio
from .assemblyai_client import transcribe_from_url


class SpotifyClient:
    """Handle Spotify episode transcription"""
    
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.sp = None
        
        if self.client_id and self.client_secret:
            auth_manager = SpotifyClientCredentials(
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
    
    def get_episode_info(self, episode_id: str) -> Optional[Dict]:
        """Get episode info from Spotify"""
        try:
            if not self.sp:
                return None
            
            episode = self.sp.episode(episode_id)
            return {
                "title": episode["name"],
                "show": episode["show"]["name"],
                "description": episode["description"],
                "audio_url": episode.get("audio_preview_url"),
                "duration_ms": episode.get("duration_ms"),
                "release_date": episode.get("release_date"),
                "image": episode["show"]["images"][0]["url"] if episode["show"]["images"] else None
            }
        except Exception as e:
            print(f"Error fetching Spotify episode: {e}")
            return None
    
    def extract_episode_id(self, spotify_url: str) -> Optional[str]:
        """Extract episode ID from Spotify URL"""
        # URL format: https://open.spotify.com/episode/EPISODE_ID
        try:
            parts = spotify_url.split("/episode/")
            if len(parts) == 2:
                episode_id = parts[1].split("?")[0]
                return episode_id
        except:
            pass
        return None


class PodcastClient:
    """Handle generic podcast support (RSS feeds)"""
    
    @staticmethod
    async def get_podcast_episode_from_url(feed_url: str) -> Optional[Dict]:
        """Extract podcast episode info from RSS feed URL"""
        try:
            import feedparser
            
            feed = feedparser.parse(feed_url)
            
            if not feed.entries:
                return None
            
            # Get first/latest episode
            entry = feed.entries[0]
            
            # Find audio link
            audio_url = None
            for link in entry.get("links", []):
                if "audio" in link.get("type", "").lower():
                    audio_url = link.get("href")
                    break
            
            # Fallback to enclosure
            if not audio_url and entry.get("enclosures"):
                audio_url = entry["enclosures"][0].get("href")
            
            return {
                "title": entry.get("title", "Unknown"),
                "show": feed.feed.get("title", "Unknown Podcast"),
                "description": entry.get("summary", ""),
                "audio_url": audio_url,
                "published": entry.get("published", ""),
                "duration": entry.get("duration", "Unknown"),
                "image": feed.feed.get("image", {}).get("href")
            }
        except Exception as e:
            print(f"Error fetching podcast episode: {e}")
            return None


async def ingest_spotify_episode(episode_url: str, video_id: str) -> Optional[str]:
    """
    Ingest a Spotify episode
    
    Args:
        episode_url: Spotify episode URL
        video_id: Unique identifier for this media
    
    Returns:
        Transcript or None if failed
    """
    try:
        client = SpotifyClient()
        episode_id = client.extract_episode_id(episode_url)
        
        if not episode_id:
            return None
        
        episode_info = client.get_episode_info(episode_id)
        
        if not episode_info or not episode_info.get("audio_url"):
            return None
        
        # Get full audio from AssemblyAI
        transcript = await transcribe_from_url(episode_info["audio_url"], video_id)
        
        return transcript
    except Exception as e:
        print(f"Error ingesting Spotify episode: {e}")
        return None


async def ingest_podcast_episode(podcast_url: str, video_id: str) -> Optional[str]:
    """
    Ingest a podcast episode from RSS feed
    
    Args:
        podcast_url: RSS feed URL or direct episode URL
        video_id: Unique identifier for this media
    
    Returns:
        Transcript or None if failed
    """
    try:
        episode_info = await PodcastClient.get_podcast_episode_from_url(podcast_url)
        
        if not episode_info or not episode_info.get("audio_url"):
            return None
        
        # Get full audio transcription
        transcript = await transcribe_from_url(episode_info["audio_url"], video_id)
        
        return transcript
    except Exception as e:
        print(f"Error ingesting podcast episode: {e}")
        return None


def parse_streaming_url(url: str) -> Optional[str]:
    """
    Identify if URL is Spotify, Podcast, or other streaming platform
    
    Returns:
        'spotify', 'podcast', 'youtube', or None
    """
    if "spotify.com" in url:
        return "spotify"
    elif "podcast" in url.lower() or url.endswith(".rss"):
        return "podcast"
    elif "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    
    return None
