const express = require("express");
const transcriptService = require("../services/transcriptService");
const qaService = require("../services/qaService");

const router = express.Router();

// Hackathon MVP storage: one loaded video at a time, kept in memory.
let currentVideo = {
  youtubeUrl: null,
  transcript: "",
  chunks: [],
  source: null,
};

router.post("/load-video", async (req, res, next) => {
  try {
    const { youtubeUrl, manualTranscript } = req.body;

    if (!youtubeUrl && !manualTranscript) {
      return res.status(400).json({
        error: "Provide youtubeUrl or manualTranscript",
      });
    }

    const result = await transcriptService.loadTranscript({
      youtubeUrl,
      manualTranscript,
    });

    currentVideo = {
      youtubeUrl: youtubeUrl || null,
      transcript: result.transcript,
      chunks: result.chunks,
      source: result.source,
    };

    return res.json({
      status: "loaded",
      source: result.source,
      chunks: result.chunks.length,
    });
  } catch (error) {
    if (error.code === "NO_TRANSCRIPT") {
      return res.status(404).json({
        error: "No captions found. Please send manualTranscript in /load-video.",
      });
    }

    return next(error);
  }
});

router.post("/ask", (req, res) => {
  const { question } = req.body;

  if (!currentVideo.chunks.length) {
    return res.status(400).json({
      error: "Load a video or manual transcript first",
    });
  }

  if (!question) {
    return res.status(400).json({
      error: "question is required",
    });
  }

  const answer = qaService.answerQuestion(question, currentVideo.chunks);
  return res.json({ answer });
});

router.get("/summary", (req, res) => {
  if (!currentVideo.chunks.length) {
    return res.status(400).json({
      error: "Load a video or manual transcript first",
    });
  }

  const summary = qaService.createSummary(currentVideo.chunks);
  return res.json({ summary });
});

module.exports = router;
