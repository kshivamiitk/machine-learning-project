import dotenv from 'dotenv';
import connectDB from '../src/database/connection.js';
import { User } from '../src/models/User.js';

dotenv.config({ path: '../.env.local' });

const run = async () => {
  await connectDB();
  const created = await User.create({ name: 'Ada Lovelace', email: 'ada@example.com' });
  console.log('Created:', created.toJSON());

  const found = await User.findOne({ email: 'ada@example.com' });
  console.log('Found:', found?.toJSON());

  await User.updateOne({ email: 'ada@example.com' }, { role: 'instructor' });
  const updated = await User.findById(created._id);
  console.log('Updated role:', updated.role);

  await User.deleteOne({ _id: created._id });
  console.log('Deleted');

  process.exit(0);
};

run().catch((error) => {
  console.error(error);
  process.exit(1);
});
