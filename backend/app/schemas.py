from pydantic import BaseModel
from typing import Optional

# Base properties expected when reading or writing
class ProjectBase(BaseModel):
    title: str
    description: str
    github_url: Optional[str] = None
    live_url: Optional[str] = None

# Properties specifically required to create a new project
class ProjectCreate(ProjectBase):
    pass

# Properties returned to the frontend (includes the database ID)
class Project(ProjectBase):
    id: int

    class Config:
        from_attributes = True