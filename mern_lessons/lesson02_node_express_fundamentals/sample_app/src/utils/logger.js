export const logger = (message, context = {}) => {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${message}`, context);
};
