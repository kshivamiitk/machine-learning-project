# Lesson 06: Full-Stack Integration and State Synchronization

## Objectives
- Connect the React frontend to the Express API with shared validation and DTOs.
- Manage optimistic updates and error states across the stack.
- Introduce global state management for authenticated user sessions.

## Prerequisites
- Working REST API from Lesson 04.
- React frontend with data fetching from Lesson 05.

## 1. Cross-Layer Contracts
Create reusable TypeScript type definitions or JSON Schemas to ensure both backend and frontend agree on payload shapes. Even in JavaScript projects, you can maintain schema files:
```json
// contracts/user.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "User",
  "type": "object",
  "properties": {
    "_id": { "type": "string" },
    "name": { "type": "string" },
    "email": { "type": "string", "format": "email" },
    "role": { "type": "string" }
  },
  "required": ["_id", "name", "email"],
  "additionalProperties": false
}
```
Use AJV on the backend to validate outgoing responses in development.

## 2. Handling API Errors Gracefully
Enhance the Express error handler to send consistent JSON:
```js
app.use((err, req, res, next) => {
  const status = err.status || 500;
  res.status(status).json({
    message: err.message || 'Server error',
    details: err.details || null,
  });
});
```

On the frontend, create a helper to surface errors:
```js
// src/hooks/useApiError.js
import { useState, useCallback } from 'react';

export const useApiError = () => {
  const [error, setError] = useState(null);
  const captureError = useCallback((err) => {
    setError(err.response?.data?.message || 'Unexpected error');
  }, []);
  const resetError = () => setError(null);
  return { error, captureError, resetError };
};
```

## 3. Implementing Mutations with Optimistic Updates
Leverage React Query mutations for create/update/delete actions:
```js
// src/hooks/useCreateUser.js
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../services/apiClient.js';

export const useCreateUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload) => apiClient.post('/users', payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
  });
};
```

Add optimistic updates for a better UX:
```js
useMutation({
  mutationFn: (payload) => apiClient.patch(`/users/${payload.id}`, payload),
  onMutate: async (payload) => {
    await queryClient.cancelQueries({ queryKey: ['users'] });
    const previous = queryClient.getQueryData(['users']);
    queryClient.setQueryData(['users'], (old = []) =>
      old.map((user) => (user._id === payload.id ? { ...user, ...payload } : user))
    );
    return { previous };
  },
  onError: (_err, _payload, context) => {
    if (context?.previous) queryClient.setQueryData(['users'], context.previous);
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['users'] });
  },
});
```

## 4. Authentication State Container
Introduce a context to store the current user and tokens:
```jsx
// src/providers/AuthProvider.jsx
import { createContext, useContext, useState, useEffect } from 'react';
import { apiClient } from '../services/apiClient.js';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient
      .get('/auth/me')
      .then(({ data }) => setUser(data))
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  const value = { user, setUser, loading };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};
```

Wrap `AppProviders` with `AuthProvider` and update components to react to authentication state.

## 5. Shared Utilities
- Extract environment configuration into `config.js` on both client and server.
- Implement logging middleware on the client to track API performance.
- Share constants (e.g., roles) between layers via a `shared/` directory or npm workspace package.

## 6. Exercises
1. Implement server-side response validation using AJV and log schema mismatches.
2. Add global toast notifications to display success/error feedback in the UI.
3. Synchronize pagination state between the URL query string and React Query cache.

## Further Reading
- [Managing Remote State](https://tkdodo.eu/blog/practical-react-query)
- [Effective Full-Stack Type Sharing](https://www.totaltypescript.com/workshops/total-typescript-typesafety)
