# Lesson 02: Node.js and Express Fundamentals

## Objectives
- Practice modern JavaScript patterns in a Node.js context.
- Build a minimal Express server with environment-based configuration.
- Understand middleware, routing, and error handling flow.

## Prerequisites
- Completed Lesson 01 project setup.
- Comfort with ES6 modules or CommonJS syntax.

## 1. Reviewing Modern JavaScript Features
Ensure your backend codebase is configured for ES modules (`"type": "module"` in `package.json`). Practice these core patterns:

```js
// src/utils/logger.js
export const logger = (message, context = {}) => {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${message}`, context);
};
```

- Use `const`/`let`, arrow functions, destructuring, optional chaining, and template literals.
- Organize code into modules for testability and reuse.

## 2. Creating the Express Server Entry Point
Create `src/index.js`:

```js
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

import { router as healthRouter } from './routes/health.js';
import { logger } from './utils/logger.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 4000;

app.use(cors());
app.use(express.json());

app.use('/health', healthRouter);

app.use((err, req, res, next) => {
  logger('Unhandled error', { error: err });
  res.status(err.status || 500).json({ message: err.message || 'Server Error' });
});

app.listen(PORT, () => {
  logger(`Server listening on http://localhost:${PORT}`);
});
```

## 3. Defining Routes and Middleware
Create a basic router to verify the server works:

```js
// src/routes/health.js
import { Router } from 'express';

export const router = Router();

router.get('/', (req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});
```

Add a custom middleware to illustrate request lifecycle:

```js
// src/middleware/requestTimer.js
export const requestTimer = (req, res, next) => {
  const start = performance.now();
  res.on('finish', () => {
    const duration = (performance.now() - start).toFixed(2);
    console.info(`${req.method} ${req.originalUrl} - ${duration}ms`);
  });
  next();
};
```

Attach the middleware before routes with `app.use(requestTimer);`.

## 4. Environment Management
Create `.env` in the backend root:
```
PORT=4000
MONGO_URI=mongodb://127.0.0.1:27017/mern_course
```

Load configuration through `dotenv` and avoid committing secrets.

## 5. Exercises
1. Add a new `/api/version` endpoint that reads `APP_VERSION` from `process.env`.
2. Implement a global 404 handler returning JSON with available routes.
3. Configure ESLint + Prettier to enforce consistent code style.

## Further Reading
- [Express Guide](https://expressjs.com/en/guide/routing.html)
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
