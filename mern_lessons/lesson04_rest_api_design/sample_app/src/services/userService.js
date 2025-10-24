import { User } from '../models/User.js';

export const listUsers = async ({ page = 1, limit = 10 }) => {
  const skip = (page - 1) * limit;
  const [items, total] = await Promise.all([
    User.find().skip(skip).limit(limit).sort({ createdAt: -1 }),
    User.countDocuments(),
  ]);
  return { items, total, page, pages: Math.ceil(total / limit) };
};

export const createUser = (payload) => User.create(payload);
export const getUserById = (id) => User.findById(id);
export const updateUser = (id, payload) =>
  User.findByIdAndUpdate(id, payload, { new: true, runValidators: true });
export const deleteUser = (id) => User.findByIdAndDelete(id);
