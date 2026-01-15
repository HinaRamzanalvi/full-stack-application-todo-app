# Deployment Guide for Full Stack Todo Application

## Issue
Your Vercel deployment is showing a 404 error because you have a fullstack application (frontend + backend) but are trying to deploy it to Vercel, which only hosts frontend applications.

## Solution
You need to deploy your frontend and backend separately:

### Step 1: Deploy Backend API
Deploy your FastAPI backend to a service that supports Python applications:

#### Option A: Deploy to Render
1. Create an account at https://render.com
2. Create a new Web Service
3. Connect to your GitHub repository
4. Choose Python runtime
5. Set the build command: `pip install -r requirements.txt`
6. Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Add environment variables:
   - `DATABASE_URL`: your PostgreSQL connection string
   - `BETTER_AUTH_SECRET`: your secret key for JWT

#### Option B: Deploy to Railway
1. Create an account at https://railway.app
2. Import your repository
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Configure environment variables

### Step 2: Deploy Frontend to Vercel
1. Go to https://vercel.com and create an account
2. Create a new project and import your repository
3. In the project settings, add these environment variables:
   - `NEXT_PUBLIC_API_BASE_URL`: URL of your deployed backend API (e.g., `https://your-backend-app.onrender.com`)
   - `NEXT_PUBLIC_BETTER_AUTH_URL`: Same as above
4. Make sure you're deploying only the `frontend` directory

### Step 3: Alternative - Docker Deployment
Instead of separating frontend and backend, you could also deploy the entire application using Docker:

1. Use Docker Compose locally or deploy to a service that supports multi-container apps
2. Or containerize the frontend and serve it separately from the backend

### Step 4: Current Status
I have restored the missing backend files that were accidentally deleted:
- `backend/database/config.py`
- `backend/database/session.py`
- `backend/database/__init__.py`
- `backend/middleware/auth.py`
- `backend/middleware/__init__.py`

I also updated the requirements.txt to include PyJWT which was missing.

## Important Notes
- Your frontend (Next.js) makes API calls to your backend (FastAPI) using the `NEXT_PUBLIC_API_BASE_URL` environment variable
- When deployed separately, ensure your backend API is CORS-enabled to accept requests from your frontend domain
- Update the CORS settings in your backend's `main.py` to include your frontend's domain