---
title: Todo Backend API
emoji: 📝
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Todo Backend API

This is a FastAPI-based backend for the Todo application, designed to run on Hugging Face Spaces.

## Features

- RESTful API for todo task management (create, read, update, delete)
- User authentication and authorization
- Secure password hashing
- CORS enabled for frontend integration
- PostgreSQL database integration
- Runs on port 7860 as required by Hugging Face Spaces

## API Endpoints

- `GET /` - Health check endpoint
- `GET /health` - Health check endpoint
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `GET /api/tasks` - Get all user tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status

## Environment Variables

The following environment variables should be configured in Hugging Face Spaces:

- `DATABASE_URL`: PostgreSQL database connection string (e.g., postgresql://username:password@host:port/database)
- `BETTER_AUTH_SECRET`: Secret key for JWT token signing
- `DB_ECHO_SQL`: Set to "True" to enable SQL query logging (optional)
- `DB_POOL_SIZE`: Database connection pool size (optional, default: 20)
- `DB_MAX_OVERFLOW`: Maximum database connections overflow (optional, default: 30)

## Docker Configuration

This application is configured to run on port 7860 as required by Hugging Face Spaces.
