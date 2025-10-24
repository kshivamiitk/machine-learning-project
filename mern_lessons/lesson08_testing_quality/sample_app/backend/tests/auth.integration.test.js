import request from 'supertest';
import app from '../src/app.js';
import { User } from '../src/models/User.js';

describe('Auth flow', () => {
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
});
