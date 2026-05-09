import chromadb

def get_summary(video_id):
    try:
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_collection(name="transcripts")
        results = collection.get(where={"video_id": video_id}, limit=5)  # first 5 chunks
        texts = [m['text'] for m in results['metadatas']]
        summary = " ".join(texts)
    except Exception as e:
        print(f"Summary failed: {e}, using fallback")
        global fallback_store
        if 'fallback_store' not in globals():
            fallback_store = []
        chunks = [c for c in fallback_store if c['video_id'] == video_id][:5]
        summary = " ".join([c['text'] for c in chunks])
    return summary