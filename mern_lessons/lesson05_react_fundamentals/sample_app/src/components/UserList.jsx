import { useUsers } from '../hooks/useUsers.js';

export const UserList = () => {
  const { data = [], isLoading, isError } = useUsers();

  if (isLoading) return <p>Loading users...</p>;
  if (isError) return <p>Unable to load users.</p>;

  return (
    <ul>
      {data.map((user) => (
        <li key={user._id}>
          {user.name} — {user.email}
        </li>
      ))}
    </ul>
  );
};
