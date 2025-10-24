# Lesson 03: MongoDB and Data Modeling Basics

## Objectives
- Install and configure MongoDB for local development or connect to MongoDB Atlas.
- Practice CRUD operations with the MongoDB shell and Mongoose ODM.
- Design simple schemas and discuss document modeling best practices.

## Prerequisites
- Backend server from Lesson 02 running locally.
- MongoDB server available (local or Atlas cluster).

## 1. Installing MongoDB
- macOS: `brew tap mongodb/brew && brew install mongodb-community@7.0`
- Windows: Use the official MSI installer and enable the MongoDB service.
- Linux: Follow distro-specific instructions from MongoDB docs.

Verify the service:
```bash
mongod --version
mongo --eval "db.runCommand({ ping: 1 })"
```

## 2. Connecting with Mongoose
Install Mongoose (already added in Lesson 01). Create `src/database/connection.js`:
```js
import mongoose from 'mongoose';

const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI, {
      serverSelectionTimeoutMS: 5000,
    });
    console.log('MongoDB connected');
  } catch (error) {
    console.error('Mongo connection error', error);
    process.exit(1);
  }
};

export default connectDB;
```

Invoke `connectDB()` in your server entry point before `app.listen`.

## 3. Defining a Schema and Model
Create a simple `User` model:
```js
// src/models/User.js
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
```

Discuss key schema design concepts:
- Favor embedding for data accessed together, referencing for separate lifecycles.
- Use `timestamps` and `indexes` for performance.
- Validate data at the schema layer to simplify controllers.

## 4. Practicing CRUD Operations
Create a playground script `scripts/userPlayground.js`:
```js
import dotenv from 'dotenv';
import connectDB from '../src/database/connection.js';
import { User } from '../src/models/User.js';

dotenv.config();

const run = async () => {
  await connectDB();
  const created = await User.create({ name: 'Ada Lovelace', email: 'ada@example.com' });
  console.log('Created:', created.toJSON());

  const found = await User.findOne({ email: 'ada@example.com' });
  console.log('Found:', found);

  await User.updateOne({ email: 'ada@example.com' }, { role: 'instructor' });
  const updated = await User.findById(created._id);
  console.log('Updated:', updated.role);

  await User.deleteOne({ _id: created._id });
  console.log('Deleted');

  process.exit(0);
};

run().catch((error) => {
  console.error(error);
  process.exit(1);
});
```

Execute with `node scripts/userPlayground.js`.

## 5. Exercises
1. Add schema validation for password hashes and ensure they are not selected by default.
2. Create a `Course` model referencing `User` as instructor.
3. Seed the database with multiple users using `User.insertMany`.

## Further Reading
- [MongoDB Data Modeling](https://www.mongodb.com/developer/products/mongodb/schema-design-best-practices/)
- [Mongoose Guides](https://mongoosejs.com/docs/guide.html)
