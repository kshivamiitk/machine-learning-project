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
