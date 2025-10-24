import createHttpError from 'http-errors';
import {
  listUsers,
  createUser,
  getUserById,
  updateUser,
  deleteUser,
} from '../services/userService.js';

export const getUsers = async (req, res, next) => {
  try {
    const { page = 1, limit = 10 } = req.query;
    const result = await listUsers({ page: Number(page), limit: Number(limit) });
    res.json(result);
  } catch (error) {
    next(error);
  }
};

export const postUser = async (req, res, next) => {
  try {
    const created = await createUser(req.body);
    res.status(201).json(created);
  } catch (error) {
    next(error);
  }
};

export const getUser = async (req, res, next) => {
  try {
    const user = await getUserById(req.params.id);
    if (!user) throw createHttpError(404, 'User not found');
    res.json(user);
  } catch (error) {
    next(error);
  }
};

export const patchUser = async (req, res, next) => {
  try {
    const user = await updateUser(req.params.id, req.body);
    if (!user) throw createHttpError(404, 'User not found');
    res.json(user);
  } catch (error) {
    next(error);
  }
};

export const removeUser = async (req, res, next) => {
  try {
    const deleted = await deleteUser(req.params.id);
    if (!deleted) throw createHttpError(404, 'User not found');
    res.status(204).end();
  } catch (error) {
    next(error);
  }
};
