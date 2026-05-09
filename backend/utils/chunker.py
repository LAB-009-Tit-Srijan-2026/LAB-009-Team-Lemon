def chunk_transcript(transcript, segments, chunk_duration=25, overlap=5):
    chunks = []
    current_start = 0
    while current_start < segments[-1]['end'] if segments else len(transcript.split()) * 0.5:
        current_end = current_start + chunk_duration
        chunk_text = ""
        for seg in segments:
            if seg['start'] >= current_start and seg['end'] <= current_end:
                chunk_text += seg['text'] + " "
        if not chunk_text:
            # Fallback if no segments
            words = transcript.split()
            start_word = int(current_start / 0.5)
            end_word = int(current_end / 0.5)
            chunk_text = " ".join(words[start_word:end_word])
        chunks.append({
            "text": chunk_text.strip(),
            "start": current_start,
            "end": current_end
        })
        current_start += chunk_duration - overlap
    return chunks