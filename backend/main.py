from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database.session import engine # Assuming you have a Base in your models
# In a real app, your SQLAlchemy models would define a `Base`.
# For now, let's create a placeholder if you don't have one.
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# --- Application Setup ---
app = FastAPI(
    title="Production Todo API",
    version="1.0.0",
)

# --- CORS Middleware ---
# This allows your frontend (running on a different domain) to communicate
# with your backend. You should restrict the origins in a real production environment.
origins = ["*"] # For development. For production, use ["https://your-frontend-domain.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Initialization ---
def init_db():
    """
    Initializes the database. In a production environment, you would use
    Alembic migrations instead of `create_all`.
    """
    try:
        # This creates tables for all models that inherit from `Base`.
        print("Initializing database and creating tables...")
        Base.metadata.create_all(bind=engine)
        print("Database initialization complete.")
    except Exception as e:
        print(f"An error occurred during database initialization: {e}")
        # Depending on the error, you might want to exit the application
        # if the database is essential for startup.
        raise

@app.on_event("startup")
def on_startup():
    init_db()

# --- API Endpoints ---
@app.get("/", tags=["Health Check"])
def read_root():
    """A simple health check endpoint."""
    return {"status": "ok", "message": "API is running"}

# Example of a route using the database dependency
# from .database.session import get_db
# @app.get("/items")
# def read_items(db: Session = Depends(get_db)):
#     # You can now use the `db` session to query the database
#     return {"message": "Database session is working"}
