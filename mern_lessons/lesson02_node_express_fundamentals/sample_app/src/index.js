import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

import { router as healthRouter } from './routes/health.js';
import { requestTimer } from './middleware/requestTimer.js';
import { logger } from './utils/logger.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 4000;

app.use(cors());
app.use(express.json());
app.use(requestTimer);

app.use('/health', healthRouter);

app.use((err, req, res, next) => {
  logger('Unhandled error', { error: err });
  res.status(err.status || 500).json({ message: err.message || 'Server Error' });
});

app.listen(PORT, () => {
  logger(`Server listening on http://localhost:${PORT}`);
});
