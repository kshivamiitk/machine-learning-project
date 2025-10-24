export const requestTimer = (req, res, next) => {
  const start = performance.now();
  res.on('finish', () => {
    const duration = (performance.now() - start).toFixed(2);
    console.info(`${req.method} ${req.originalUrl} - ${duration}ms`);
  });
  next();
};
