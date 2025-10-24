import { render, screen } from '@testing-library/react';
import { vi } from 'vitest';
import { UserList, withQueryProvider } from '../components/UserList.jsx';

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

test('renders user list', () => {
  render(withQueryProvider(<UserList />));
  expect(screen.getByText(/Ada Lovelace/)).toBeInTheDocument();
  expect(screen.getByText(/Alan Turing/)).toBeInTheDocument();
});
