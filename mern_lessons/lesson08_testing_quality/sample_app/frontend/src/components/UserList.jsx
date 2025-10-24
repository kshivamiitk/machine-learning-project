import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useUsers } from '../hooks/useUsers.js';

const queryClient = new QueryClient();

export const UserList = () => {
  const { data = [], isLoading, isError } = useUsers();

  if (isLoading) return <p>Loading users...</p>;
  if (isError) return <p>Unable to load users.</p>;

  return (
    <ul>
      {data.map((user) => (
        <li key={user._id}>{user.name}</li>
      ))}
    </ul>
  );
};

export const withQueryProvider = (component) => (
  <QueryClientProvider client={queryClient}>{component}</QueryClientProvider>
);
