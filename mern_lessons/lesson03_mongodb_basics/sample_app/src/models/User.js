import mongoose from 'mongoose';

const userSchema = new mongoose.Schema(
  {
    name: { type: String, required: true, trim: true },
    email: { type: String, required: true, unique: true, lowercase: true },
    role: { type: String, enum: ['student', 'instructor'], default: 'student' },
  },
  { timestamps: true }
);

export const User = mongoose.model('User', userSchema);
