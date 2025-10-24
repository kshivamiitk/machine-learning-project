import { Container, PageHeading } from '../components/Layout.jsx';
import { UserList } from '../components/UserList.jsx';

export const DashboardPage = () => (
  <Container>
    <PageHeading title="Dashboard" subtitle="Welcome to the MERN course portal" />
    <p>Select a section to begin learning.</p>
    <UserList />
  </Container>
);
