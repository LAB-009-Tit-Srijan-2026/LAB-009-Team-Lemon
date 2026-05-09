from sentence_transformers import SentenceTransformer
import chromadb
import re
from .utils.chunker import chunk_transcript
from .utils.transcript_loader import load_transcript

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    YouTubeTranscriptApi = None


def _extract_youtube_id(url: str) -> str | None:
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11})(?:[&?]|$)",
        r"youtu\.be\/([0-9A-Za-z_-]{11})(?:[&?]|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def _load_youtube_transcript(url: str):
    if not YouTubeTranscriptApi:
        print("YouTubeTranscriptApi not installed; skipping YouTube subtitle load.")
        return None
    video_id = _extract_youtube_id(url)
    if not video_id:
        return None
    try:
        api = YouTubeTranscriptApi()
        entries = api.fetch(video_id)
        return list(entries)
    except Exception as e:
        print(f"YouTube subtitle load failed: {e}")
        return None


def _get_entry_value(entry, key, default=""):
    if isinstance(entry, dict):
        return entry.get(key, default)
    return getattr(entry, key, default)


def _create_segments_from_entries(entries):
    segments = []
    for entry in entries:
        text = str(_get_entry_value(entry, "text", "")).strip()
        if not text:
            continue
        start = float(_get_entry_value(entry, "start", 0.0) or 0.0)
        duration = float(_get_entry_value(entry, "duration", 0.0) or 0.0)
        end = start + duration if duration > 0 else start + 2.0
        segments.append({"text": text, "start": start, "end": end})
    return segments


def ingest_video(video_url, video_id):
    transcript = None
    segments = []
    if video_url and ("youtube.com" in video_url or "youtu.be" in video_url):
        entries = _load_youtube_transcript(video_url)
        if entries:
            segments = _create_segments_from_entries(entries)
            transcript = " ".join([seg["text"] for seg in segments])

    if not transcript:
        transcript = load_transcript()
        segments = [{"text": transcript, "start": 0.0, "end": len(transcript.split()) * 0.5}]

    chunks = chunk_transcript(transcript, segments)
    try:
        model_emb = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model_emb.encode([c['text'] for c in chunks])
    except Exception as e:
        print(f"Embeddings failed: {e}, using keyword fallback")
        embeddings = None

    try:
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_or_create_collection(name="transcripts")
        for i, chunk in enumerate(chunks):
            metadata = {
                "text": chunk['text'],
                "start_time": chunk['start'],
                "end_time": chunk['end'],
                "video_id": video_id
            }
            if embeddings is not None:
                collection.add(
                    ids=[f"{video_id}_{i}"],
                    embeddings=[embeddings[i]],
                    metadatas=[metadata]
                )
            else:
                collection.add(
                    ids=[f"{video_id}_{i}"],
                    metadatas=[metadata]
                )
    except Exception as e:
        print(f"ChromaDB failed: {e}, storing in memory")
        global fallback_store
        if 'fallback_store' not in globals():
            fallback_store = []
        for chunk in chunks:
            fallback_store.append({
                "text": chunk['text'],
                "start_time": chunk['start'],
                "end_time": chunk['end'],
                "video_id": video_id
            })
