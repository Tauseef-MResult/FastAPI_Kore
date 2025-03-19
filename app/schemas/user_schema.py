from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    employee_id: str = Field(min_length=1)
    name: str = Field(min_length=2)
    email: EmailStr
    user_type: str = Field(pattern="^(admin|employee)$")

    class Config:
        extra = "forbid"  #Not allowing any other params apart from above in request body
        from_attributes = True  # Not needed for MongoDB, as it is non-ORM


class UserResponse(UserBase):
    id: str


class AuthRequest(BaseModel):
    employee_id: str = Field(min_length=1)
    password: str = Field(min_length=3)

    class Config:
        extra = "forbid"

