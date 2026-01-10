# Hackathon II Todo App

A full-stack web application for managing tasks with user authentication and multi-user support.

## Features

- User authentication (signup/login)
- Create, read, update, and delete tasks
- Filter tasks by completion status
- Sort tasks by title or creation date
- Responsive design for desktop and mobile

## Tech Stack

### Backend
- Python 3.11+
- FastAPI
- SQLModel
- PostgreSQL
- JWT for authentication

### Frontend
- Next.js 16+
- TypeScript
- Tailwind CSS
- Better Auth

## Setup

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Start the backend server:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.local.example .env.local
# Edit .env.local with your configuration
```

4. Start the frontend development server:
```bash
npm run dev
```

## API Endpoints

- `GET /api/tasks` - Get all tasks for the authenticated user
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a specific task
- `DELETE /api/tasks/{id}` - Delete a specific task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status

## Environment Variables

### Backend (.env)
- `DATABASE_URL` - PostgreSQL connection string
- `BETTER_AUTH_SECRET` - Secret key for JWT signing

### Frontend (.env.local)
- `NEXT_PUBLIC_BETTER_AUTH_URL` - Base URL for auth
- `NEXT_PUBLIC_API_BASE_URL` - Base URL for API

## Architecture

The application follows a micro-frontend architecture with separate backend and frontend services:

- **Frontend**: Next.js app with App Router
- **Backend**: FastAPI with SQLModel ORM
- **Database**: PostgreSQL with proper indexing
- **Authentication**: JWT-based with stateless verification
- **Data Isolation**: All queries filtered by user_id

## Security

- JWT-based authentication
- All endpoints require valid tokens
- Data isolation between users
- Input validation and sanitization

## Development

The project is organized as follows:

```
backend/
├── main.py                 # FastAPI application entry point
├── models/                 # SQLModel definitions
├── database/               # Database session and config
├── api/                    # API routes and dependencies
├── middleware/             # Authentication middleware
└── requirements.txt        # Python dependencies

frontend/
├── package.json            # Node.js dependencies
├── next.config.js          # Next.js configuration
├── src/
│   ├── app/                # Next.js App Router pages
│   ├── components/         # React components
│   ├── lib/                # Utility functions
│   └── styles/             # Global styles
└── tsconfig.json           # TypeScript configuration
```

## Running with Docker

A `docker-compose.yml` file is provided for easy setup:

```bash
docker-compose up
```

This will start PostgreSQL, the backend, and the frontend services.