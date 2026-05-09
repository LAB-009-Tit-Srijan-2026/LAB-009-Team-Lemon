import chromadb
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from utils.similarity import keyword_similarity

def ask_question(video_id, question, history=[]):
    try:
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_collection(name="transcripts")
        # Query for video_id
        results = collection.get(where={"video_id": video_id})
        if not results['ids']:
            raise Exception("No data found")
        texts = results['metadatas']
        embeddings = results['embeddings']
    except Exception as e:
        print(f"ChromaDB failed: {e}, using fallback")
        global fallback_store
        if 'fallback_store' not in globals():
            fallback_store = []
        texts = [c for c in fallback_store if c['video_id'] == video_id]
        embeddings = None

    if embeddings:
        # Use embeddings
        model_emb = SentenceTransformer('all-MiniLM-L6-v2')
        q_emb = model_emb.encode([question])[0]
        similarities = cosine_similarity([q_emb], embeddings)[0]
        best_idx = np.argmax(similarities)
    elif texts:
        # Use cosine on texts if no embeddings
        model_emb = SentenceTransformer('all-MiniLM-L6-v2')
        text_embs = model_emb.encode([t['text'] for t in texts])
        q_emb = model_emb.encode([question])[0]
        similarities = cosine_similarity([q_emb], text_embs)[0]
        best_idx = np.argmax(similarities)
    else:
        # Keyword matching
        similarities = [keyword_similarity(question, t['text']) for t in texts]
        best_idx = np.argmax(similarities)

    best_chunk = texts[best_idx]
    answer = best_chunk['text']
    timestamps = [best_chunk['start_time'], best_chunk['end_time']]
    return answer, timestamps