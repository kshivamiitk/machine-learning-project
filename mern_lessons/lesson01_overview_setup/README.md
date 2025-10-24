# Lesson 01: MERN Stack Overview and Environment Setup

## Objectives
- Understand the components of the MERN stack and how they interact.
- Install the core tooling required for full-stack JavaScript development.
- Scaffold a monorepo-style project structure that will grow throughout the curriculum.

## Prerequisites
- Basic familiarity with JavaScript syntax and Git workflows.
- Node.js (v18+) and npm installed on your machine.

## 1. Understanding the MERN Stack
The **MERN** stack is composed of four technologies:
- **MongoDB**: NoSQL document database storing application data as JSON-like documents.
- **Express.js**: Backend web framework for Node.js that simplifies HTTP routing and middleware.
- **React**: Front-end library for building interactive user interfaces.
- **Node.js**: JavaScript runtime for executing server-side code.

These components form an opinionated, full-stack JavaScript workflow:
1. React renders the UI, issuing HTTP requests to the backend.
2. Express (running on Node.js) handles the requests, applying business logic.
3. MongoDB persists data and returns query results to the API.
4. The API responds with JSON to the React client, completing the cycle.

## 2. Installing Core Tooling
1. **Node.js and npm**: Verify installation with `node -v` and `npm -v`.
2. **MongoDB Community Server** or **MongoDB Atlas** account for cloud-hosted databases.
3. **npx create-react-app** or **Vite** for bootstrapping React apps.
4. **VS Code** (recommended) with extensions:
   - ESLint
   - Prettier
   - MongoDB for VS Code
5. Optional but useful utilities: `nodemon`, `concurrently`, `pnpm`.

## 3. Project Skeleton
Create a directory to contain both client and server projects:
```bash
mkdir mern-tutorial
cd mern-tutorial
mkdir backend frontend
```

Initialize the Node.js backend:
```bash
cd backend
npm init -y
npm install express dotenv cors mongoose
npm install --save-dev nodemon
```

Initialize the React front-end (using Vite for speed):
```bash
cd ../frontend
npm create vite@latest . -- --template react
npm install
```

## 4. Recommended npm Scripts
Update `backend/package.json` to include helper scripts:
```json
"scripts": {
  "dev": "nodemon src/index.js",
  "start": "node src/index.js",
  "lint": "eslint ."
}
```

Update `frontend/package.json`:
```json
"scripts": {
  "dev": "vite",
  "build": "vite build",
  "preview": "vite preview"
}
```

## 5. Next Steps
- Configure environment variables with `.env` files on both client and server.
- Install MongoDB locally or create a cluster on Atlas.
- Proceed to Lesson 02 to build foundational Node.js and Express skills.

## Further Reading
- [Official MERN Stack documentation (MongoDB)](https://www.mongodb.com/mern-stack)
- [Node.js Guides](https://nodejs.org/en/docs/guides/)
- [React Documentation](https://react.dev/learn)
