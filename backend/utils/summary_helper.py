import re
from typing import List, Tuple

def extract_topics(text: str, num_topics: int = 5) -> List[str]:
    """Extract key topics from text using simple heuristics."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    topics = []
    seen = set()
    for sentence in sentences[:20]:
        words = sentence.lower().split()
        key_words = [w for w in words if len(w) > 5 and w not in {'about', 'which', 'would', 'there', 'their', 'these'}]
        if key_words:
            topic = ' '.join(key_words[:3])
            if topic not in seen:
                topics.append(sentence[:100])
                seen.add(topic)
                if len(topics) >= num_topics:
                    break
    return topics

def summarize_by_topics(text: str, chunks: List[dict]) -> List[dict]:
    """Create topic-wise summaries from chunks."""
    if not chunks:
        return []
    topics = extract_topics(text, num_topics=5)
    result = []
    for i, topic in enumerate(topics):
        relevant_chunks = []
        for chunk in chunks:
            chunk_text = chunk.get('text', '').lower()
            if any(word in chunk_text for word in topic.lower().split()[:2]):
                relevant_chunks.append(chunk)
        if relevant_chunks:
            summary_text = ' '.join([c.get('text', '')[:150] for c in relevant_chunks[:2]])
            result.append({
                'topic': topic[:80],
                'summary': summary_text,
                'timestamp': relevant_chunks[0].get('start', 0)
            })
    return result

def get_last_n_minutes_summary(chunks: List[dict], minutes: int = 5) -> Tuple[str, float]:
    """Get summary of last N minutes based on timestamps."""
    if not chunks:
        return ("No content available", 0)
    last_chunk = chunks[-1]
    end_time = last_chunk.get('end', 0)
    start_time = end_time - (minutes * 60)
    relevant_chunks = [
        c for c in chunks
        if c.get('end', 0) > start_time
    ]
    if relevant_chunks:
        summary_text = ' '.join([c.get('text', '') for c in relevant_chunks])
        return (summary_text[:500], relevant_chunks[0].get('start', end_time))
    return (' '.join([c.get('text', '') for c in chunks[-3:]]), end_time - 300)

def format_timestamp(seconds: float) -> str:
    """Format seconds to HH:MM:SS."""
    seconds = max(0, seconds)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"
