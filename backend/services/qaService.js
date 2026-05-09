const STOP_WORDS = new Set([
  "a",
  "an",
  "and",
  "are",
  "as",
  "at",
  "be",
  "by",
  "for",
  "from",
  "how",
  "in",
  "is",
  "it",
  "of",
  "on",
  "or",
  "that",
  "the",
  "this",
  "to",
  "what",
  "when",
  "where",
  "why",
  "with",
]);

function keywords(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .split(/\s+/)
    .filter((word) => word.length > 2 && !STOP_WORDS.has(word));
}

function scoreChunk(questionKeywords, chunk) {
  const chunkWords = new Set(keywords(chunk));
  return questionKeywords.reduce((score, word) => {
    return score + (chunkWords.has(word) ? 1 : 0);
  }, 0);
}

function answerQuestion(question, chunks) {
  const questionKeywords = keywords(question);

  if (!questionKeywords.length) {
    return chunks[0] || "I could not find an answer in the transcript.";
  }

  const bestMatch = chunks
    .map((chunk) => ({
      chunk,
      score: scoreChunk(questionKeywords, chunk),
    }))
    .sort((a, b) => b.score - a.score)[0];

  if (!bestMatch || bestMatch.score === 0) {
    return "I could not find a clearly relevant answer in the transcript.";
  }

  return bestMatch.chunk;
}

function createSummary(chunks) {
  const usefulChunks = chunks.slice(0, 3);
  return usefulChunks.join(" ");
}

module.exports = {
  answerQuestion,
  createSummary,
  keywords,
};
