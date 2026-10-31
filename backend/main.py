
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create the FastAPI application
app = FastAPI(
    title="Sandcastle API",
    description="Backend API for managing preview environments",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to Sandcastle API",
        "status": "running"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "sandcastle-backend"
    }

# Temporary preview environment data
preview_environments = [
    {
        "id": 1,
        "repository": "payment-service",
        "pull_request": 42,
        "status": "running"
    },
    {
        "id": 2,
        "repository": "user-dashboard",
        "pull_request": 18,
        "status": "building"
    }
]


# Get all preview environments
@app.get("/environments")
def get_environments():
    return {
        "total": len(preview_environments),
        "environments": preview_environments
    }
