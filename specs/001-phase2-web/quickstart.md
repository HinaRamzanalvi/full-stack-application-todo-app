# Quickstart Guide: Hackathon II Todo – Phase II: Full-Stack Web Application

## Prerequisites

- Node.js 18+ with npm
- Python 3.11+
- PostgreSQL (or Docker for containerized setup)
- Git

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env file with your configuration
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### 4. Database Setup
```bash
# Make sure PostgreSQL is running
# Create database and run migrations (if using Alembic)
cd backend
python -c "from database.session import engine; from models.task import Task; Task.metadata.create_all(engine)"
```

### 5. Environment Variables
Create `.env` files in both frontend and backend with the following:

**Backend (.env):**
```
DATABASE_URL=postgresql://username:password@localhost:5432/todoapp
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
```

**Frontend (.env.local):**
```
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Running the Application

### Development Mode

**Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

### Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Better Auth: Integrated in frontend

## Testing the Application

1. Open http://localhost:3000 in your browser
2. Click "Sign Up" to create a new account
3. Verify your account and log in
4. Create a new task using the form
5. Verify that the task appears in your task list
6. Try marking the task as complete
7. Test filtering and sorting features
8. Log out and log in with a different account to verify data isolation

## Common Commands

**Backend:**
- Run tests: `pytest`
- Format code: `black .`
- Lint code: `flake8 .`

**Frontend:**
- Run tests: `npm test`
- Build for production: `npm run build`
- Format code: `npm run format`
- Lint code: `npm run lint`

## Troubleshooting

### Common Issues:

1. **Database Connection Issues**: Verify DATABASE_URL is correct in backend .env
2. **Authentication Issues**: Check that BETTER_AUTH_SECRET matches between frontend and backend
3. **API Connection Issues**: Ensure frontend NEXT_PUBLIC_API_BASE_URL points to running backend
4. **JWT Validation Issues**: Verify both services use the same secret for token validation