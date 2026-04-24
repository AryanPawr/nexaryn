# Nexaryn

Nexaryn is a local-first agentic cybersecurity platform. This repository is scaffolded as a Docker Compose monorepo for the locked stack:

- Frontend: Next.js in `/frontend`
- Backend: FastAPI in `/backend`
- Agent and worker: Python in `/agent`
- Data services: PostgreSQL and Redis

## Local Setup

Create a local environment file, review the safe development defaults, then start the stack:

```sh
cp .env.example .env
make up
```

The initial scaffold starts all five services without application implementation files. Follow-up backend, frontend, and agent tasks will replace the scaffold commands with real Next.js, FastAPI, and worker entrypoints.

## Services

- `frontend`: Node-based scaffold for the Next.js app, published on `FRONTEND_PORT` (`3002` by default)
- `backend`: Python-based scaffold for the FastAPI app, published on `BACKEND_PORT` (`8000` by default)
- `worker`: Python background worker scaffold for telemetry processing
- `postgres`: PostgreSQL with persistent named volume `postgres_data`, published on `POSTGRES_PORT` (`5432` by default)
- `redis`: Redis, published on `REDIS_PORT` (`6379` by default)

## Common Commands

```sh
make up       # start the full local stack
make down     # stop and remove local containers
make logs     # follow service logs
make migrate  # verify database access until migrations are added
```
