from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import engine, get_db

# This line automatically creates your database tables when the app starts
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Website API")

# Setup CORS to allow your Next.js frontend to communicate securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # Local Development
        "https://sahibshakhayev.tech",    # Production
        "https://www.sahibshakhayev.tech"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Backend and Database are connected and running!"}

# Endpoint to fetch all projects
@app.get("/projects/", response_model=List[schemas.Project])
def get_projects(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    projects = db.query(models.Project).offset(skip).limit(limit).all()
    return projects

# Endpoint to add a new project
@app.post("/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project