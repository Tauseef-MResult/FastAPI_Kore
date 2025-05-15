from pydantic import BaseModel, Field
from datetime import datetime

class EvaluationBase(BaseModel):
    idea_id: str = Field(pattern=r"^IDEA_[0-9]+$")
    evaluator_id: str = Field(min_length=1, pattern=r"^\d+$")
    feasibility_score: float = Field(ge=0.0, le=10.0)
    impact_score: float = Field(ge=0.0, le=10.0)
    resource_score: float = Field(ge=0.0, le=10.0)
    status: str = Field(pattern="^(Accepted|Rejected)$")
    comments: str = Field(min_length=2)

    class Config:
        extra = "forbid"  # Not allowing any other params apart from above in request body
        from_attributes = True  # Not needed for MongoDB, as it is non-ORM

class EvaluationResponse(EvaluationBase):
    evaluation_id: str = Field(min_length=1, pattern=r"^\d+$")
    evaluation_score: float
    evaluation_date: datetime