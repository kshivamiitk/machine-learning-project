#!/usr/bin/env bash
# Sample scaffold script for Lesson 01 of the MERN track.
# Run with: bash sample_scaffold.sh <project-name>
set -euo pipefail

PROJECT_NAME=${1:-mern-tutorial}

if [ -d "$PROJECT_NAME" ]; then
  echo "Directory $PROJECT_NAME already exists" >&2
  exit 1
fi

echo "Creating MERN tutorial workspace: $PROJECT_NAME"
mkdir -p "$PROJECT_NAME"/backend/src "$PROJECT_NAME"/frontend

pushd "$PROJECT_NAME"/backend >/dev/null
cat <<'JSON' > package.json
{
  "name": "mern-backend",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "nodemon src/index.js",
    "start": "node src/index.js"
  },
  "dependencies": {
    "cors": "^2.8.5",
    "dotenv": "^16.4.5",
    "express": "^4.19.2",
    "mongoose": "^8.4.0"
  },
  "devDependencies": {
    "nodemon": "^3.1.0"
  }
}
JSON
popd >/dev/null

pushd "$PROJECT_NAME"/frontend >/dev/null
cat <<'JSON' > package.json
{
  "name": "mern-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "vite": "^5.2.0"
  }
}
JSON
popd >/dev/null

echo "Scaffold complete. Install dependencies with npm install inside backend and frontend folders."
