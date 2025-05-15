from pydantic import BaseModel, Field
from datetime import datetime

class IdeaBase(BaseModel):
    employee_id: str = Field(min_length=1, pattern=r"^\d+$")
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=10, max_length=500)
    category: str = Field(pattern="^(Technology|Operations|Customer Service|Finance)$")
    impact: str = Field(min_length=10, max_length=200)

    class Config:
        extra = "forbid"  # Not allowing any other params apart from above in request body
        from_attributes = True  # Not needed for MongoDB, as it is non-ORM

class IdeaResponse(IdeaBase):
    idea_id: str = Field(pattern=r"^IDEA_[0-9]+$")
    submission_date: datetime
    status: str = Field(default="Under Review")
    evaluation_score: float = Field(default=0.0)
    comments: str = Field(min_length=2,default="NA")