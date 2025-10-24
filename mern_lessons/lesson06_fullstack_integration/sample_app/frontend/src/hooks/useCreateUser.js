import { useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../services/apiClient.js';

export const useCreateUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload) => apiClient.post('/users', payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
  });
};
