# Lesson 08: Testing Strategy and Quality Assurance

## Objectives
- Configure automated testing for backend and frontend layers.
- Write unit, integration, and end-to-end tests for critical flows.
- Integrate CI pipelines with linting, testing, and type checks.

## Prerequisites
- Authenticated application from Lesson 07.
- Basic familiarity with Jest and Testing Library.

## 1. Backend Testing with Jest and Supertest
Install dev dependencies:
```bash
cd backend
npm install --save-dev jest supertest mongodb-memory-server @types/jest
```

Configure Jest (`jest.config.js`):
```js
export default {
  testEnvironment: 'node',
  transform: {},
  setupFilesAfterEnv: ['./tests/setup.js'],
};
```

Create `tests/setup.js` to spin up an in-memory MongoDB instance:
```js
import { MongoMemoryServer } from 'mongodb-memory-server';
import mongoose from 'mongoose';

let mongod;

beforeAll(async () => {
  mongod = await MongoMemoryServer.create();
  const uri = mongod.getUri();
  await mongoose.connect(uri);
});

afterEach(async () => {
  await mongoose.connection.db.dropDatabase();
});

afterAll(async () => {
  await mongoose.connection.close();
  await mongod.stop();
});
```

Write an integration test for the auth flow:
```js
import request from 'supertest';
import app from '../src/app.js';
import { User } from '../src/models/User.js';

it('logs in with valid credentials', async () => {
  await User.create({
    name: 'Test User',
    email: 'test@example.com',
    passwordHash: await User.hashPassword('password123'),
  });

  const response = await request(app).post('/auth/login').send({
    email: 'test@example.com',
    password: 'password123',
  });

  expect(response.status).toBe(200);
  expect(response.body.accessToken).toBeDefined();
});
```

## 2. Frontend Testing with Vitest and Testing Library
Install dependencies in `frontend`:
```bash
npm install --save-dev vitest @testing-library/react @testing-library/jest-dom
```

Update `vite.config.js`:
```js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/tests/setup.js',
  },
});
```

Create `src/tests/setup.js`:
```js
import '@testing-library/jest-dom';
```

Example component test:
```jsx
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { UserList } from '../components/UserList.jsx';

vi.mock('../hooks/useUsers.js', () => ({
  useUsers: () => ({
    data: [
      { _id: '1', name: 'Ada Lovelace', email: 'ada@example.com' },
      { _id: '2', name: 'Alan Turing', email: 'alan@example.com' },
    ],
    isLoading: false,
    isError: false,
  }),
}));

const renderWithProviders = (ui) => {
  const client = new QueryClient();
  return render(<QueryClientProvider client={client}>{ui}</QueryClientProvider>);
};

test('renders user list', () => {
  renderWithProviders(<UserList />);
  expect(screen.getByText(/Ada Lovelace/)).toBeInTheDocument();
  expect(screen.getByText(/Alan Turing/)).toBeInTheDocument();
});
```

## 3. End-to-End Testing
Choose Playwright or Cypress. Example Playwright setup:
```bash
npm init playwright@latest
```

Create tests simulating login, navigation, and CRUD operations against a running local stack.

## 4. Continuous Integration Pipeline
Use GitHub Actions `.github/workflows/ci.yml`:
```yaml
name: CI

on: [push, pull_request]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    services:
      mongo:
        image: mongo:7
        ports: ['27017:27017']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18
      - run: npm ci
        working-directory: backend
      - run: npm run test -- --runInBand
        working-directory: backend
      - run: npm ci
        working-directory: frontend
      - run: npm run test -- --run
        working-directory: frontend
```

## 5. Quality Gates
- Enforce coverage thresholds with Jest/Vitest.
- Add lint checks (`npm run lint`) and type checks (TypeScript or JSDoc) to CI.
- Require pull requests to pass CI before merging.

## 6. Exercises
1. Implement contract tests ensuring API responses match JSON Schemas.
2. Add visual regression testing with Storybook + Chromatic or Playwright.
3. Configure Danger.js to automate code review reminders (e.g., missing tests).

## Further Reading
- [Testing JavaScript.com](https://testingjavascript.com/)
- [Playwright Docs](https://playwright.dev/docs/intro)
