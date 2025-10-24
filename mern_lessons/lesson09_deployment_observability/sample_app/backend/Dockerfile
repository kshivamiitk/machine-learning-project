FROM node:18-alpine AS base
WORKDIR /app
COPY package*.json ./
RUN npm install --only=production
COPY . .
CMD ["node", "src/index.js"]
