import { Router } from 'express';
import jwt from 'jsonwebtoken';
import createHttpError from 'http-errors';
import { User } from '../models/User.js';

const router = Router();

const generateTokens = (user) => {
  const payload = { sub: user._id, role: user.role };
  const accessToken = jwt.sign(payload, process.env.JWT_SECRET, { expiresIn: '15m' });
  const refreshToken = jwt.sign(payload, process.env.JWT_REFRESH_SECRET, { expiresIn: '7d' });
  return { accessToken, refreshToken };
};

router.post('/login', async (req, res, next) => {
  try {
    const { email, password } = req.body;
    const user = await User.findOne({ email }).select('+passwordHash');
    if (!user || !(await user.comparePassword(password))) {
      throw createHttpError(401, 'Invalid credentials');
    }

    const tokens = generateTokens(user);
    res.cookie('refreshToken', tokens.refreshToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 7 * 24 * 60 * 60 * 1000,
    });
    res.json({
      accessToken: tokens.accessToken,
      user: { id: user._id, name: user.name, role: user.role },
    });
  } catch (error) {
    next(error);
  }
});

router.post('/refresh', (req, res, next) => {
  try {
    const token = req.cookies.refreshToken;
    if (!token) throw createHttpError(401, 'Missing refresh token');
    const payload = jwt.verify(token, process.env.JWT_REFRESH_SECRET);
    const accessToken = jwt.sign({ sub: payload.sub, role: payload.role }, process.env.JWT_SECRET, { expiresIn: '15m' });
    res.json({ accessToken });
  } catch (error) {
    next(error);
  }
});

router.post('/logout', (req, res) => {
  res.clearCookie('refreshToken');
  res.status(204).end();
});

router.get('/me', async (req, res, next) => {
  try {
    const user = await User.findById(req.user.sub).select('name email role');
    res.json(user);
  } catch (error) {
    next(error);
  }
});

export { router };
