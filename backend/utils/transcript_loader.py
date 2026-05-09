from pathlib import Path

def load_transcript():
    base = Path(__file__).resolve().parent.parent
    transcript_path = base / 'data' / 'transcript.txt'
    try:
        return transcript_path.read_text(encoding='utf-8')
    except Exception:
        return "Fallback transcript text here."
