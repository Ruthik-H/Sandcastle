
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

import models
from database import SessionLocal


# Request models
class EnvironmentCreate(BaseModel):
    repository: str
    pull_request: int
    status: str


class EnvironmentUpdate(BaseModel):
    status: str


# Create FastAPI application
app = FastAPI(
    title="Sandcastle API",
    description="Backend API for managing preview environments",
    version="1.0.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to Sandcastle API",
        "status": "running"
    }


# Fetch all environments
@app.get("/environments")
def get_environments(db: Session = Depends(get_db)):
    environments = db.query(models.Environment).all()

    return {
        "total": len(environments),
        "environments": [
            {
                "id": env.id,
                "repository": env.repository,
                "pull_request": env.pull_request,
                "status": env.status
            }
            for env in environments
        ]
    }


# Create a new environment
@app.post("/environments")
def create_environment(
    environment: EnvironmentCreate,
    db: Session = Depends(get_db)
):
    new_environment = models.Environment(
        repository=environment.repository,
        pull_request=environment.pull_request,
        status=environment.status
    )

    db.add(new_environment)
    db.commit()
    db.refresh(new_environment)

    return {
        "message": "Environment created successfully",
        "environment": {
            "id": new_environment.id,
            "repository": new_environment.repository,
            "pull_request": new_environment.pull_request,
            "status": new_environment.status
        }
    }


# Update an existing environment
@app.patch("/environments/{environment_id}")
def update_environment(
    environment_id: int,
    environment: EnvironmentUpdate,
    db: Session = Depends(get_db)
):
    db_environment = (
        db.query(models.Environment)
        .filter(models.Environment.id == environment_id)
        .first()
    )

    if db_environment is None:
        return {"message": "Environment not found"}

    db_environment.status = environment.status

    db.commit()
    db.refresh(db_environment)

    return {
        "message": "Environment updated successfully",
        "environment": {
            "id": db_environment.id,
            "repository": db_environment.repository,
            "pull_request": db_environment.pull_request,
            "status": db_environment.status
        }
    }


# Delete an existing environment
@app.delete("/environments/{environment_id}")
def delete_environment(
    environment_id: int,
    db: Session = Depends(get_db)
):
    environment = (
        db.query(models.Environment)
        .filter(models.Environment.id == environment_id)
        .first()
    )

    if environment is None:
        return {"message": "Environment not found"}

    db.delete(environment)
    db.commit()

    return {
        "message": "Environment deleted successfully"
    }


# Initial GitHub webhook receiver
@app.post("/webhooks/github")
async def github_webhook(request: Request):
    payload = await request.json()

    print("GitHub webhook received!")
    print(payload)

    return {
        "message": "GitHub webhook received successfully"
    }
