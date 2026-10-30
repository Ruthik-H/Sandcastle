
from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI(
    title="Sandcastle API",
    description="Backend API for managing preview environments",
    version="1.0.0"
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
