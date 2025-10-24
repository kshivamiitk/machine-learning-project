# Lesson 07: Authentication, Authorization, and Security Hardening

## Objectives
- Implement JWT-based authentication with refresh tokens.
- Protect routes with middleware and role-based access control.
- Apply security best practices on both client and server.

## Prerequisites
- User model from Lesson 03 including password hashes.
- Integrated frontend from Lesson 06.

## 1. Password Storage
Update the `User` schema to include password hashing:
```js
import bcrypt from 'bcryptjs';

const userSchema = new mongoose.Schema({
  passwordHash: { type: String, required: true, select: false },
});

userSchema.methods.comparePassword = function comparePassword(password) {
  return bcrypt.compare(password, this.passwordHash);
};

userSchema.statics.hashPassword = (password) => bcrypt.hash(password, 12);
```

Ensure registration controller uses `User.hashPassword(req.body.password)` before saving.

## 2. Auth Routes
Create `src/routes/authRoutes.js`:
```js
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
    res.json({ accessToken: tokens.accessToken, user: { id: user._id, name: user.name, role: user.role } });
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
```

## 3. Authentication Middleware
Create `src/middleware/auth.js`:
```js
import jwt from 'jsonwebtoken';
import createHttpError from 'http-errors';

export const authenticate = (req, _res, next) => {
  const header = req.headers.authorization;
  if (!header?.startsWith('Bearer ')) {
    return next(createHttpError(401, 'Missing bearer token'));
  }
  const token = header.split(' ')[1];
  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    next();
  } catch (error) {
    next(createHttpError(401, 'Invalid or expired token'));
  }
};

export const authorize = (...allowedRoles) => (req, _res, next) => {
  if (!allowedRoles.includes(req.user.role)) {
    return next(createHttpError(403, 'Insufficient permissions'));
  }
  next();
};
```

Apply middleware to routes: `router.get('/', authenticate, authorize('instructor'), getUsers);`

## 4. Client-Side Auth Flow
- Store the access token in memory or `localStorage` with refresh fallback.
- Intercept 401 responses and call `/auth/refresh` to renew tokens.
- Update `AuthProvider` to persist the access token and attach it to `apiClient` headers:
```js
apiClient.interceptors.request.use((config) => {
  const token = authStore.getAccessToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
```

## 5. Security Hardening Checklist
- Enable Helmet middleware for HTTP headers.
- Rate-limit login attempts with `express-rate-limit`.
- Sanitize user input with `express-mongo-sanitize` and `xss-clean`.
- Enforce HTTPS in production, secure cookies, and CSRF protection for sensitive endpoints.
- Use environment variables for secrets and rotate them periodically.

## 6. Exercises
1. Implement password reset flow using signed tokens and email delivery (use Nodemailer).
2. Add two-factor authentication with TOTP (e.g., `speakeasy`).
3. Write integration tests covering login, refresh, and protected resource access.

## Further Reading
- [OWASP Top Ten](https://owasp.org/www-project-top-ten/)
- [JWT Best Practices](https://auth0.com/blog/a-look-at-the-latest-draft-for-jwt-bcp/)
