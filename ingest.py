import os
import tempfile
import yt_dlp
import assemblyai as aai
from sentence_transformers import SentenceTransformer
import chromadb
from dotenv import load_dotenv

# Load environment variables (e.g., ASSEMBLYAI_API_KEY)
load_dotenv()

def ingest_youtube_video(url: str, video_id: str = None) -> list[str]:
    """
    Robust ingestion pipeline for a YouTube URL:
    1. Downloads audio as temporary .m4a
    2. Transcribes using AssemblyAI
    3. Chunks transcript into 30s windows with 5s overlap
    4. Embeds chunks using sentence-transformers
    5. Stores embeddings and metadata in ChromaDB
    6. Deletes temporary audio file
    Returns a list of inserted chunk IDs.
    """
    # Extract video_id from URL if not provided
    if video_id is None:
        if "v=" in url:
            video_id = url.split("v=")[-1].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[-1].split("?")[0]
        else:
            video_id = "unknown_video"

    # 1. Download the best audio format as a temporary local .m4a file
    temp_audio_file = tempfile.NamedTemporaryFile(suffix=".m4a", delete=False).name
    try:
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': temp_audio_file,
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }],
        }
        print(f"Downloading audio for {url}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # 2. Transcribe using AssemblyAI Python SDK
        print("Transcribing audio with AssemblyAI...")
        # Make sure ASSEMBLYAI_API_KEY is set in your environment variables
        aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
        if not aai.settings.api_key:
            raise ValueError("ASSEMBLYAI_API_KEY environment variable is not set")
            
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(temp_audio_file)
        
        if transcript.error:
            raise Exception(f"AssemblyAI Transcription failed: {transcript.error}")

        words = transcript.words
        if not words:
            print("No words found in transcription.")
            return []

        # 3. Chunk transcript into 30-second windows with 5-second overlap
        print("Chunking transcript...")
        chunks = []
        window_size_ms = 30000  # 30 seconds
        overlap_ms = 5000       # 5 seconds overlap
        step_size_ms = window_size_ms - overlap_ms
        
        total_duration_ms = words[-1].end
        
        for start_window in range(0, total_duration_ms, step_size_ms):
            end_window = start_window + window_size_ms
            
            # Find words that start within this time window
            chunk_words = [w for w in words if start_window <= w.start < end_window]
            
            if chunk_words:
                chunk_text = " ".join([w.text for w in chunk_words])
                chunks.append({
                    "text": chunk_text,
                    "start_time": chunk_words[0].start / 1000.0, # Convert to seconds
                    "end_time": chunk_words[-1].end / 1000.0,    # Convert to seconds
                })

        # 4. Embed chunks using sentence-transformers (all-MiniLM-L6-v2)
        print("Embedding chunks...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        texts = [c["text"] for c in chunks]
        embeddings = model.encode(texts).tolist()

        # 5. Store vector embeddings along with metadata in ChromaDB
        print("Storing embeddings in ChromaDB...")
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_or_create_collection(name="transcripts")
        
        ids = [f"{video_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "chunk_text": c["text"],
                "start_time": c["start_time"],
                "end_time": c["end_time"],
                "video_id": video_id
            }
            for c in chunks
        ]
        
        # Add to collection
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
        
        print(f"Successfully inserted {len(ids)} chunks.")
        return ids

    finally:
        # Ensure temporary audio file is deleted
        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)
            print(f"Deleted temporary audio file: {temp_audio_file}")

if __name__ == "__main__":
    # Example usage:
    # url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
    # inserted_ids = ingest_youtube_video(url)
    # print("Inserted IDs:", inserted_ids)
    pass
