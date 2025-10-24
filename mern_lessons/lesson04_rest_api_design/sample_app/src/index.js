import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { errors } from 'celebrate';

import connectDB from './database/connection.js';
import { router as userRouter } from './routes/userRoutes.js';
import { logger } from './utils/logger.js';

dotenv.config({ path: '../.env.local' });

const app = express();
const PORT = process.env.PORT || 4000;

app.use(cors());
app.use(express.json());

app.use('/api/users', userRouter);
app.use(errors());

app.use((err, req, res, next) => {
  logger('Unhandled error', { error: err });
  res.status(err.status || 500).json({ message: err.message || 'Server Error' });
});

const start = async () => {
  await connectDB();
  app.listen(PORT, () => logger(`API listening on http://localhost:${PORT}`));
};

start();

export default app;
