# Lesson 09: Deployment, Monitoring, and Operational Excellence

## Objectives
- Containerize the MERN application for consistent deployment.
- Configure cloud infrastructure for hosting the frontend, backend, and database.
- Implement logging, monitoring, and alerting to maintain production health.

## Prerequisites
- Completed functionality from Lessons 01–08.
- Docker installed locally and a cloud provider account (Render, Railway, Fly.io, AWS, etc.).

## 1. Containerization Strategy
Create Dockerfiles for both backend and frontend.

**Backend `Dockerfile`:**
```dockerfile
FROM node:18-alpine AS base
WORKDIR /app
COPY package*.json ./
RUN npm install --only=production
COPY . .
CMD ["node", "src/index.js"]
```

**Frontend `Dockerfile`:**
```dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
```

Use Docker Compose to orchestrate services:
```yaml
version: '3.9'
services:
  api:
    build: ./backend
    ports:
      - '4000:4000'
    environment:
      - MONGO_URI=${MONGO_URI}
      - JWT_SECRET=${JWT_SECRET}
      - JWT_REFRESH_SECRET=${JWT_REFRESH_SECRET}
    depends_on:
      - mongo
  client:
    build: ./frontend
    ports:
      - '5173:80'
  mongo:
    image: mongo:7
    volumes:
      - mongo-data:/data/db
volumes:
  mongo-data:
```

## 2. Cloud Deployment Options
- **Render/Railway/Fly.io**: Simple deployment from GitHub repo with managed MongoDB add-ons.
- **AWS ECS + Fargate**: Deploy containers behind an Application Load Balancer. Use DocumentDB or Atlas for MongoDB.
- **Vercel + Render**: Host the frontend on Vercel, backend on Render, database on Atlas.

Ensure environment variables are configured securely via platform secrets managers.

## 3. Continuous Deployment Pipeline
Extend CI workflow with deployment jobs triggered on main branch merges:
```yaml
jobs:
  deploy:
    needs: build-and-test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: ghcr.io/<org>/mern-backend:latest
      - name: Trigger Render Deploy Hook
        run: curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
```

## 4. Observability
- **Logging**: Use `winston` or `pino` on the backend. Ship logs to a central service (LogDNA, Datadog, ELK).
- **Metrics**: Expose Prometheus-compatible metrics via `/metrics` using `prom-client` for backend, and track frontend vitals via Google Analytics or Sentry.
- **Tracing**: Integrate OpenTelemetry for distributed tracing across backend services.
- **Monitoring Dashboard**: Configure Grafana or provider-native dashboards for CPU, memory, response times, and error rates.

## 5. Alerting and Incident Response
- Configure alert rules (e.g., error rate > 5%, latency > 1s) tied to Slack or PagerDuty.
- Document a runbook outlining triage steps, rollback procedures, and contact points.
- Schedule regular game days to practice incident response.

## 6. Operational Best Practices
- Automate database backups and test restoration.
- Use feature flags (LaunchDarkly, ConfigCat) for gradual rollouts.
- Implement blue/green or canary deployments for safer releases.
- Regularly review dependency vulnerabilities with `npm audit` or `snyk`.

## 7. Exercises
1. Deploy the stack to your preferred platform and verify HTTPS endpoints.
2. Add health checks to the backend (`/healthz`, `/readyz`) and configure load balancer probes.
3. Instrument the backend with OpenTelemetry and visualize traces in Jaeger.

## Further Reading
- [Twelve-Factor App](https://12factor.net/)
- [OpenTelemetry](https://opentelemetry.io/docs/instrumentation/js/)
- [MongoDB Production Checklist](https://www.mongodb.com/developer/products/mongodb/production-best-practices/)
