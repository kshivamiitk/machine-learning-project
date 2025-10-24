# Lesson 04: RESTful API Design with Express and Mongoose

## Objectives
- Structure the backend with controllers, services, and routers.
- Implement CRUD endpoints backed by MongoDB models.
- Apply validation, error handling, and pagination best practices.

## Prerequisites
- MongoDB connection and User model from Lesson 03.
- Familiarity with Express routing and middleware from Lesson 02.

## 1. Project Structure
Recommended backend folders:
```
src/
  controllers/
  routes/
  models/
  services/
  middleware/
  utils/
```

This separation keeps route definitions slim and business logic isolated.

## 2. Creating a Service Layer
`src/services/userService.js`:
```js
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
export const updateUser = (id, payload) => User.findByIdAndUpdate(id, payload, { new: true, runValidators: true });
export const deleteUser = (id) => User.findByIdAndDelete(id);
```

## 3. Controllers and Error Handling
`src/controllers/userController.js`:
```js
import createHttpError from 'http-errors';
import { listUsers, createUser, getUserById, updateUser, deleteUser } from '../services/userService.js';

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
```

## 4. Routing and Validation
Use a router with Joi validation middleware:

```js
// src/routes/userRoutes.js
import { Router } from 'express';
import { celebrate, Joi, Segments } from 'celebrate';
import { getUsers, postUser, getUser, patchUser, removeUser } from '../controllers/userController.js';

export const router = Router();

router.get('/', getUsers);
router.post(
  '/',
  celebrate({
    [Segments.BODY]: Joi.object({
      name: Joi.string().min(2).required(),
      email: Joi.string().email().required(),
      role: Joi.string().valid('student', 'instructor'),
    }),
  }),
  postUser
);
router.get('/:id', getUser);
router.patch('/:id', patchUser);
router.delete('/:id', removeUser);
```

Remember to mount the router: `app.use('/api/users', userRouter);`

## 5. Error Middleware and Celebrate Integration
Add Celebrate error handler:
```js
import { errors } from 'celebrate';
app.use(errors());
```

Keep the custom error middleware from Lesson 02 after Celebrate for consistent responses.

## 6. Exercises
1. Add query parameter validation for pagination.
2. Implement soft deletes by setting `deletedAt` and filtering queries.
3. Extend the API with `Course` CRUD endpoints referencing instructors.

## Further Reading
- [REST API Design Guidelines](https://martinfowler.com/articles/richardsonMaturityModel.html)
- [Celebrate (Joi middleware)](https://github.com/arb/celebrate)
