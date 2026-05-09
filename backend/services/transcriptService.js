const { YoutubeTranscript } = require("youtube-transcript");

function cleanText(text) {
  return text
    .replace(/\s+/g, " ")
    .replace(/\[.*?\]/g, "")
    .trim();
}

function splitIntoChunks(text, wordsPerChunk = 80) {
  const words = cleanText(text).split(" ").filter(Boolean);
  const chunks = [];

  for (let i = 0; i < words.length; i += wordsPerChunk) {
    const chunk = words.slice(i, i + wordsPerChunk).join(" ");

    if (chunk.length > 20) {
      chunks.push(chunk);
    }
  }

  return chunks;
}

function flattenTranscript(items) {
  return items
    .map((item) => item.text || "")
    .join(" ");
}

async function fetchYoutubeTranscript(youtubeUrl) {
  try {
    // youtube-transcript uses YouTube's public caption data.
    // It may return manual or auto-generated captions depending on availability.
    const items = await YoutubeTranscript.fetchTranscript(youtubeUrl);
    const transcript = cleanText(flattenTranscript(items));

    if (!transcript) {
      return null;
    }

    return {
      transcript,
      source: "youtube-captions",
    };
  } catch (error) {
    return null;
  }
}

async function loadTranscript({ youtubeUrl, manualTranscript }) {
  if (manualTranscript) {
    const transcript = cleanText(manualTranscript);

    return {
      transcript,
      chunks: splitIntoChunks(transcript),
      source: "manual",
    };
  }

  const youtubeResult = await fetchYoutubeTranscript(youtubeUrl);

  if (!youtubeResult) {
    const error = new Error("No YouTube captions available");
    error.code = "NO_TRANSCRIPT";
    throw error;
  }

  return {
    ...youtubeResult,
    chunks: splitIntoChunks(youtubeResult.transcript),
  };
}

module.exports = {
  loadTranscript,
  cleanText,
  splitIntoChunks,
};
