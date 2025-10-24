import express from 'express';
import cookieParser from 'cookie-parser';
import jwt from 'jsonwebtoken';
import createHttpError from 'http-errors';
import { User } from './models/User.js';

const app = express();

app.use(express.json());
app.use(cookieParser());

app.post('/auth/login', async (req, res, next) => {
  try {
    const { email, password } = req.body;
    const user = await User.findOne({ email });
    if (!user || !(await user.comparePassword(password))) {
      throw createHttpError(401, 'Invalid credentials');
    }
    const token = jwt.sign({ sub: user._id }, 'test-secret');
    res.json({ accessToken: token });
  } catch (error) {
    next(error);
  }
});

app.use((err, _req, res, _next) => {
  res.status(err.status || 500).json({ message: err.message });
});

export default app;
