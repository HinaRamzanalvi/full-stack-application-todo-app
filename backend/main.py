
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database.session import init_db
from api.routes import tasks, auth
from middleware.auth import security
from database.config import settings

app = FastAPI(title="Hackathon II Todo API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Replace with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(auth.router, prefix="/api", tags=["auth"])

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()

@app.get("/")
def read_root():
    return {"message": "Hackathon II Todo API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}