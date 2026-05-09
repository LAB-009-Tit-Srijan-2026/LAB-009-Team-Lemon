def load_transcript():
    try:
        with open('./data/transcript.txt', 'r') as f:
            return f.read()
    except:
        return "Fallback transcript text here."