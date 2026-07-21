import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Use the environment variable if available (Production), 
# otherwise use the Docker Development credentials we set up earlier.
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://devuser:devpassword@db:5432/devdb"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency: This creates a fresh database session for every request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()