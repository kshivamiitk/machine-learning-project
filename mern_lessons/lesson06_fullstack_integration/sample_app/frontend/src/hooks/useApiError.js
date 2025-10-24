import { useState, useCallback } from 'react';

export const useApiError = () => {
  const [error, setError] = useState(null);

  const captureError = useCallback((err) => {
    setError(err.response?.data?.message || 'Unexpected error');
  }, []);

  const resetError = () => setError(null);

  return { error, captureError, resetError };
};
