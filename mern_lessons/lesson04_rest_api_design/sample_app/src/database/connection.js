import mongoose from 'mongoose';

const connectDB = async () => {
  if (!process.env.MONGO_URI) {
    throw new Error('MONGO_URI missing. Provide it via environment variable.');
  }
  await mongoose.connect(process.env.MONGO_URI);
  console.log('MongoDB connected');
};

export default connectDB;
