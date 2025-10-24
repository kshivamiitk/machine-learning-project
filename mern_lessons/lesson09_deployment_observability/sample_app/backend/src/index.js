import express from 'express';

const app = express();
app.get('/healthz', (_req, res) => {
  res.json({ status: 'ok' });
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`API listening on ${PORT}`);
});
