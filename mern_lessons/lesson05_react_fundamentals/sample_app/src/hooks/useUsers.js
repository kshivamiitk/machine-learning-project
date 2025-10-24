import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../services/apiClient.js';

const fetchUsers = async () => {
  const { data } = await apiClient.get('/users');
  return data.items ?? [];
};

export const useUsers = () => useQuery({ queryKey: ['users'], queryFn: fetchUsers });
