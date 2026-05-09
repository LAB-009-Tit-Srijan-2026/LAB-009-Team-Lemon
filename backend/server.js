const express = require("express");
const apiRoutes = require("./routes/apiRoutes");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json({ limit: "2mb" }));

app.get("/", (req, res) => {
  res.json({
    service: "AI Learning Companion",
    status: "ok",
    endpoints: ["POST /load-video", "POST /ask", "GET /summary"],
  });
});

app.use("/", apiRoutes);

app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({
    error: "Something went wrong",
    details: err.message,
  });
});

app.listen(PORT, () => {
  console.log(`AI Learning Companion backend running on http://localhost:${PORT}`);
});
