# DevTrack

A production-shaped issue tracker API, built with **FastAPI**, **PostgreSQL**, **Redis**, and **Docker** — developed as a learning project to build real backend engineering skills: API design, database modeling, authentication, caching, testing, and containerization.

> **Status: Feature-complete backend, pre-deployment.** Every core phase of the project is built and tested. Only deployment and final documentation polish remain.

## Tech Stack

- **Python** + **FastAPI** — API framework
- **PostgreSQL** — relational database
- **SQLAlchemy** — ORM
- **Alembic** — database migrations
- **Pydantic** — request/response validation
- **JWT** (python-jose) + **passlib/bcrypt** — authentication
- **Redis** — caching
- **Docker** + **Docker Compose** — containerization
- **pytest** — testing
- **uv** — dependency and environment management

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

Redis sits alongside this stack, caching read-heavy list
endpoints and invalidating on writes.
```

Database schema changes are tracked and versioned using Alembic migrations. The entire stack (app, PostgreSQL, Redis) runs together via Docker Compose, with services addressing each other by name over a shared Docker network.

## Data Model

```
User
  └── owns → Project (creator_id FK)
                └── has → Issue (project_id FK, indexed)
                            └── has → Comment (issue_id FK, indexed)
```

Deleting a `User` cascades through Projects → Issues → Comments automatically via SQLAlchemy relationships.

## Features

### Authentication
- Register (`POST /register`) and login (`POST /login`, OAuth2 password flow — compatible with the Swagger `/docs` Authorize button)
- Passwords hashed with bcrypt, never stored in plain text
- JWT access tokens (30-minute expiry) protect all write operations
- `GET /me` returns the currently authenticated user

### Projects, Issues, Comments
- Full CRUD (Create, List, Get-by-ID, Update, Delete) for all three resources
- Foreign-key-enforced relationships with cascading deletes
- Ownership tied to real authenticated users (no placeholder data)

### Filtering, Search, Pagination
- `GET /issues` supports filtering by `status` and `priority`, case-insensitive partial text search across title/description, and `limit`/`offset` pagination
- `GET /projects` supports the same text search and pagination pattern

### Caching
- `GET /projects` results are cached in Redis (60s expiry) and automatically invalidated on create/update/delete

### Error Handling & Logging
- Centralized exception handlers return a consistent `{"error": ...}` shape for both application errors and validation failures
- Structured logging (timestamps, severity levels) instead of ad-hoc prints

### Testing
- Separate test database, isolated from development data
- Unit tests covering authentication logic and all three repository layers
- Integration test verifying the real HTTP stack via FastAPI's TestClient

## Known Design Decisions

- `Issue.creator` and `Comment.creator` store the author's email as plain text rather than a foreign key to `User`. Since both already link back to a `Project` (which does have a real `creator_id` FK), this was a deliberate simplification rather than an oversight.
- Redis caching currently covers `GET /projects` only; `Issue`/`Comment` reads are not yet cached.

## Not Yet Implemented

- Deployment to a public host/domain
- "Get all issues owned by a user" (would require a SQL join across Project → Issue)
- Rate limiting

## Running Locally (Docker — recommended)

**Prerequisites:** Docker Desktop

```bash
git clone https://github.com/midas0715/devtrack.git
cd devtrack

# Create a .env file in the project root:
# DATABASE_URL=postgresql://postgres:<password>@db:5432/devtrack
# REDIS_URL=redis://redis:6379
# SECRET_KEY=<a long random string>

docker compose up --build

# In a separate terminal, run migrations against the containerized database:
docker exec -it devtrack-app-1 uv run alembic upgrade head
```

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

## Running Locally (without Docker)

**Prerequisites:** Python 3.12+, PostgreSQL, Redis, [uv](https://docs.astral.sh/uv/)

```bash
uv sync
psql -U postgres -c "CREATE DATABASE devtrack;"
uv run alembic upgrade head
uv run uvicorn devtrack.main:app --reload
```

## Running Tests

```bash
uv run pytest -v
```

Requires a separate `devtrack_test` PostgreSQL database and a `TEST_DATABASE_URL` entry in `.env`.

## Project Structure

```
devtrack/
├── alembic/                 # Database migrations
├── Dockerfile
├── docker-compose.yml
├── src/devtrack/
│   ├── main.py               # FastAPI app entry point, middleware, exception handlers
│   ├── api/
│   │   ├── routes/           # Route handlers (HTTP layer)
│   │   └── dependencies.py   # get_current_user (auth dependency)
│   ├── schemas/               # Pydantic request/response models
│   ├── models/                 # SQLAlchemy database models
│   ├── repositories/           # Database access layer
│   ├── core/                   # config, security (hashing/JWT), logging, cache, redis client
│   └── database/                # Engine, session, and base config
└── tests/                       # Unit and integration tests
```