import chromadb
from .utils.summary_helper import summarize_by_topics, get_last_n_minutes_summary

def get_summary(video_id):
    try:
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_collection(name="transcripts")
        results = collection.get(where={"video_id": video_id}, limit=5)
        texts = [m['text'] for m in results['metadatas']]
        summary = " ".join([t for t in texts if t])
    except Exception as e:
        print(f"Summary failed: {e}, using fallback")
        global fallback_store
        if 'fallback_store' not in globals():
            fallback_store = []
        chunks = [c for c in fallback_store if c['video_id'] == video_id][:5]
        summary = " ".join([c['text'] for c in chunks])
    if not summary:
        return "Summary is not available yet. Please ingest a video first."
    return summary

def get_topic_summaries(video_id):
    try:
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_collection(name="transcripts")
        results = collection.get(where={"video_id": video_id})
        if not results['ids']:
            raise Exception("No data found")
        chunks = [
            {
                'text': m.get('text', ''),
                'start': m.get('start_time', 0),
                'end': m.get('end_time', 0)
            }
            for m in results['metadatas']
        ]
        full_text = " ".join([c['text'] for c in chunks])
    except Exception as e:
        print(f"Topic summary failed: {e}, using fallback")
        global fallback_store
        if 'fallback_store' not in globals():
            fallback_store = []
        chunks = [c for c in fallback_store if c['video_id'] == video_id]
        full_text = " ".join([c['text'] for c in chunks])
    
    if not chunks:
        return []
    return summarize_by_topics(full_text, chunks)

def get_last_minutes_summary(video_id, minutes: int = 5):
    try:
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_collection(name="transcripts")
        results = collection.get(where={"video_id": video_id})
        if not results['ids']:
            raise Exception("No data found")
        chunks = [
            {
                'text': m.get('text', ''),
                'start': m.get('start_time', 0),
                'end': m.get('end_time', 0)
            }
            for m in results['metadatas']
        ]
    except Exception as e:
        print(f"Last N minutes summary failed: {e}, using fallback")
        global fallback_store
        if 'fallback_store' not in globals():
            fallback_store = []
        chunks = [c for c in fallback_store if c['video_id'] == video_id]
    
    if not chunks:
        return {"summary": "No content available", "timestamp": 0}
    
    summary_text, timestamp = get_last_n_minutes_summary(chunks, minutes)
    return {"summary": summary_text, "timestamp": timestamp}
