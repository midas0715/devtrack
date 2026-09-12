# DevTrack

A production-oriented issue tracker API, built with **FastAPI** and **PostgreSQL** — developed as a learning project to build real backend engineering skills: API design, database modeling, migrations, and layered architecture (router → service/repository → database).

> **Status: Work in progress.** This project is being built incrementally, one architectural concept at a time, with an emphasis on understanding *why* each piece exists — not just shipping features. See "Progress" below for exactly what's implemented so far.

## Tech Stack

- **Python** + **FastAPI** — API framework
- **PostgreSQL** — relational database
- **SQLAlchemy** — ORM
- **Alembic** — database migrations
- **Pydantic** — request/response validation
- **uv** — dependency and environment management

Planned additions: JWT authentication, pytest test suite, Redis caching, Docker/Docker Compose.

## Architecture

```
Client
   ↓
FastAPI Router        → HTTP concerns (routes, status codes)
   ↓
Pydantic Schemas      → request/response validation
   ↓
Repository Layer      → database access (SQLAlchemy queries)
   ↓
SQLAlchemy Models      → table definitions
   ↓
PostgreSQL             → persistent storage
```

Database schema changes are tracked and versioned using Alembic migrations rather than applied manually.

## Features implemented so far

- **Projects**
  - Create a project (`POST /projects`)
  - List all projects (`GET /projects`)
- **Issues**
  - Create an issue linked to a project via foreign key (`POST /issues`)
  - List all issues (`GET /issues`)
  - Database-enforced referential integrity — an issue cannot be created against a non-existent project
- **Health check** endpoint (`GET /health`) for uptime monitoring
- Environment-based configuration (`.env`) — no secrets committed to source control
- Interactive API docs auto-generated at `/docs`

## Not yet implemented

- Get-by-ID, Update, and Delete endpoints for Projects and Issues
- Comments on issues
- User accounts and JWT-based authentication (currently, `creator` on an issue is a temporary hardcoded placeholder)
- Filtering, search, and pagination
- Automated tests (pytest)
- Redis caching
- Docker / Docker Compose setup
- Deployment

## Running locally

**Prerequisites:** Python 3.12+, PostgreSQL, [uv](https://docs.astral.sh/uv/)

```bash
# Clone the repo
git clone https://github.com/midas0715/devtrack.git
cd devtrack

# Install dependencies
uv sync

# Create a .env file in the project root:
# DATABASE_URL=postgresql://<user>:<password>@localhost:5432/devtrack

# Create the PostgreSQL database
psql -U postgres -c "CREATE DATABASE devtrack;"

# Apply migrations
uv run alembic upgrade head

# Run the server
uv run uvicorn devtrack.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

## Project structure

```
devtrack/
├── alembic/                # Database migrations
├── src/devtrack/
│   ├── main.py              # FastAPI app entry point
│   ├── api/routes/          # Route handlers (HTTP layer)
│   ├── schemas/             # Pydantic request/response models
│   ├── models/              # SQLAlchemy database models
│   ├── repositories/        # Database access layer
│   └── database/            # Engine, session, and base config
└── tests/                   # (planned)
```