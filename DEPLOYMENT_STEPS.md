# Deployment Steps for Full Stack Todo Application

## Overview
Your application consists of:
- **Frontend**: Next.js application in the `frontend/` directory
- **Backend**: FastAPI application in the `backend/` directory

Vercel can only host frontend applications, so you need to deploy these separately.

## Step-by-Step Deployment Guide

### Step 1: Deploy Backend API (Required First)

#### Option A: Deploy to Render.com
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect to your GitHub repository
4. Select your repository
5. Set the following configurations:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables:
   - `DATABASE_URL`: PostgreSQL connection string (e.g., `postgresql://user:pass@host:port/dbname`)
   - `BETTER_AUTH_SECRET`: A strong secret key for JWT (generate with `openssl rand -hex 32`)

7. Click "Create Web Service"

#### Option B: Deploy to Railway.app
1. Go to [Railway Dashboard](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Choose your repository
5. Set the following configurations:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Go to "Settings" → "Variables" and add:
   - `DATABASE_URL`: PostgreSQL connection string
   - `BETTER_AUTH_SECRET`: A strong secret key for JWT

### Step 2: Get Your Backend URL
After deployment, note your backend URL (e.g., `https://your-app.onrender.com` or `https://your-app.up.railway.app`)

### Step 3: Deploy Frontend to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your Git repository
4. **Important Configuration**:
   - **Root Directory**: Select `frontend` folder
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
5. Add Environment Variables in Project Settings:
   ```
   NEXT_PUBLIC_API_BASE_URL=https://your-backend-url.com
   NEXT_PUBLIC_BETTER_AUTH_URL=https://your-backend-url.com
   ```
   Replace `https://your-backend-url.com` with your actual backend URL from Step 2.

6. Click "Deploy"

### Step 4: Update Backend CORS Settings (After Frontend Deployment)

Once you have your frontend deployed on Vercel, update your backend's `main.py` file:

```python
# In backend/main.py, change the CORS settings:

# FROM:
allow_origins=["*"],  # TODO: Replace with your frontend domain in production

# TO (replace with your actual Vercel domain):
allow_origins=["https://your-frontend-project.vercel.app"],  # Your actual Vercel domain
```

### Step 5: Redeploy Backend
After updating CORS settings, redeploy your backend application.

## Testing Your Deployment

1. Test your backend API: Visit `https://your-backend-url.com/health`
   - Should return: `{"status": "healthy"}`

2. Test your frontend: Visit your Vercel URL
   - Should load the Todo application
   - API calls should work correctly

## Troubleshooting

### Common Issues:

1. **404 Error on Vercel**: Usually means you're trying to deploy the full stack instead of just the frontend directory
2. **API Calls Failing**: Check that `NEXT_PUBLIC_API_BASE_URL` is correctly set in Vercel environment variables
3. **CORS Errors**: Ensure your backend allows requests from your Vercel domain
4. **Login/Register Not Working**: Verify that `NEXT_PUBLIC_BETTER_AUTH_URL` is set correctly

### Debugging Steps:

1. Open browser Developer Tools (F12)
2. Check the "Network" tab for failed API requests
3. Verify that API calls are going to your backend URL, not localhost
4. Check console for any error messages

## Environment Variables Reference

### Frontend (Vercel):
- `NEXT_PUBLIC_API_BASE_URL`: Your deployed backend URL
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Same as above

### Backend (Render/Railway):
- `DATABASE_URL`: PostgreSQL database connection string
- `BETTER_AUTH_SECRET`: JWT secret key
- `PORT`: Port number (provided by hosting service)

## Redeployment Process

After making code changes:
1. Push changes to GitHub
2. Backend will auto-deploy (if configured)
3. Frontend will auto-deploy (if configured)
4. If auto-deploy is disabled, trigger manual deployment from each platform