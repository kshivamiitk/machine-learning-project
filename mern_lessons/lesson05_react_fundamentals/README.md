# Lesson 05: React Fundamentals with Modern Tooling

## Objectives
- Explore the React component model, hooks, and state management basics.
- Configure a design system and reusable UI components.
- Integrate API communication using `fetch` or `axios` with React Query.

## Prerequisites
- Frontend scaffold created in Lesson 01.
- Familiarity with JavaScript modules and JSX syntax.

## 1. Project Cleanup and Tooling
After generating the Vite React app:
- Remove boilerplate components (`App.css`, default `App.jsx`).
- Install dependencies:
  ```bash
  npm install @tanstack/react-query axios react-router-dom@6
  npm install --save-dev eslint-plugin-react-hooks eslint-plugin-react-refresh
  ```
- Configure ESLint and Prettier to match the backend style.

## 2. Structuring the Frontend
Recommended folder layout:
```
src/
  components/
  hooks/
  pages/
  providers/
  services/
  styles/
```

Create `src/providers/AppProviders.jsx`:
```jsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';

const queryClient = new QueryClient();

export const AppProviders = ({ children }) => (
  <QueryClientProvider client={queryClient}>
    <BrowserRouter>{children}</BrowserRouter>
  </QueryClientProvider>
);
```

Wrap the root component in `main.jsx`:
```jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import { AppProviders } from './providers/AppProviders.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AppProviders>
      <App />
    </AppProviders>
  </React.StrictMode>
);
```

## 3. Building Reusable UI Components
Implement a simple layout system:
```jsx
// src/components/Layout.jsx
export const Container = ({ children }) => (
  <div className="mx-auto max-w-5xl px-4 py-8">{children}</div>
);

export const PageHeading = ({ title, subtitle }) => (
  <header className="mb-6">
    <h1 className="text-3xl font-semibold text-slate-900">{title}</h1>
    {subtitle && <p className="mt-2 text-slate-600">{subtitle}</p>}
  </header>
);
```

Adopt a utility-first CSS library like Tailwind or create global styles with CSS Modules.

## 4. React Router and Pages
Define routes in `src/App.jsx`:
```jsx
import { Routes, Route, Navigate } from 'react-router-dom';
import { Container, PageHeading } from './components/Layout.jsx';

const DashboardPage = () => (
  <Container>
    <PageHeading title="Dashboard" subtitle="Welcome to the MERN course portal" />
    <p>Select a section to begin learning.</p>
  </Container>
);

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<DashboardPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
```

## 5. Fetching Data with React Query
Create `src/services/apiClient.js`:
```js
import axios from 'axios';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:4000/api',
});
```

Create a custom hook `src/hooks/useUsers.js`:
```js
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../services/apiClient.js';

const fetchUsers = async () => {
  const { data } = await apiClient.get('/users');
  return data.items;
};

export const useUsers = () => useQuery({ queryKey: ['users'], queryFn: fetchUsers });
```

Use the hook in a component:
```jsx
// src/components/UserList.jsx
import { useUsers } from '../hooks/useUsers.js';

export const UserList = () => {
  const { data, isLoading, isError } = useUsers();

  if (isLoading) return <p>Loading users...</p>;
  if (isError) return <p>Unable to load users.</p>;

  return (
    <ul>
      {data.map((user) => (
        <li key={user._id}>{user.name} — {user.email}</li>
      ))}
    </ul>
  );
};
```

## 6. Exercises
1. Add a form to create a new user and invalidate the React Query cache on success.
2. Introduce global theming (Tailwind CSS or CSS variables).
3. Configure absolute imports using Vite's `resolve.alias`.

## Further Reading
- [React Official Docs](https://react.dev/learn)
- [TanStack Query](https://tanstack.com/query/latest)
- [React Router](https://reactrouter.com/en/main)
