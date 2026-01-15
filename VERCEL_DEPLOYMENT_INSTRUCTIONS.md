# Vercel Deployment Instructions for Todo Application

## Problem
Your Vercel deployment is showing a 404 error because you have a fullstack application (frontend + backend) but are trying to deploy it to Vercel, which only hosts frontend applications.

## Solution
You need to deploy your frontend and backend separately:

### Step 1: Deploy Backend API
First, deploy your FastAPI backend to a service that supports Python applications:

#### Option A: Deploy to Render
1. Create an account at https://render.com
2. Create a new Web Service
3. Connect to your GitHub repository
4. Choose Python runtime
5. Set the build command: `pip install -r requirements.txt`
6. Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Add environment variables:
   - `DATABASE_URL`: your PostgreSQL connection string (e.g., `postgresql://username:password@host:port/dbname`)
   - `BETTER_AUTH_SECRET`: your secret key for JWT (generate a strong random key)

#### Option B: Deploy to Railway
1. Create an account at https://railway.app
2. Import your repository
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Configure environment variables as above

### Step 2: Deploy Frontend to Vercel
1. Go to https://vercel.com and create an account
2. Create a new project and import your repository
3. Make sure you're deploying only the `frontend` directory
4. In the project settings, add these environment variables:
   - `NEXT_PUBLIC_API_BASE_URL`: URL of your deployed backend API (e.g., `https://your-backend-app.onrender.com`)
   - `NEXT_PUBLIC_BETTER_AUTH_URL`: Same as above (e.g., `https://your-backend-app.onrender.com`)

### Step 3: Environment Variables Setup
In your Vercel project settings, set these environment variables:

```
NEXT_PUBLIC_API_BASE_URL=https://your-backend-app.onrender.com
NEXT_PUBLIC_BETTER_AUTH_URL=https://your-backend-app.onrender.com
```

Replace `https://your-backend-app.onrender.com` with the actual URL of your deployed backend.

### Step 4: CORS Configuration
Once you have your frontend deployed on Vercel, update the CORS settings in your backend's `main.py` to be more restrictive:

Change from:
```python
allow_origins=["*"],  # TODO: Replace with your frontend domain in production
```

To (replace with your actual Vercel domain):
```python
allow_origins=["https://your-frontend-project.vercel.app"],  # Your Vercel domain
```

## Testing the Deployment
1. First, test that your backend API is working by visiting: `https://your-backend-app.onrender.com/health`
2. You should get a response like: `{"status": "healthy"}`
3. Then test your frontend on Vercel

## Troubleshooting
- If you get CORS errors, make sure your backend allows requests from your frontend domain
- If API calls fail, verify that `NEXT_PUBLIC_API_BASE_URL` points to your live backend
- Check browser developer tools for any error messages

## Backend Endpoints
Your backend provides these API endpoints:
- `GET /health` - Health check
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/tasks` - Get user tasks
- `POST /api/tasks` - Create a task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion