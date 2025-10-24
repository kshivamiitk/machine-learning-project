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
