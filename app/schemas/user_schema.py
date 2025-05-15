from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    employee_id: str = Field(min_length=1, pattern=r"^\d+$")
    name: str = Field(min_length=2, pattern=r"^[A-Za-z ]+$")
    email: EmailStr
    user_type: str = Field(pattern=r"^(admin|employee)$")

    class Config:
        extra = "forbid"  #Not allowing any other params apart from above in request body
        from_attributes = True  # Not needed for MongoDB, as it is non-ORM


class UserResponse(UserBase):
    id: str


class AuthRequest(BaseModel):
    employee_id: str = Field(min_length=1, pattern=r"^\d+$")
    password: str = Field(min_length=3, pattern=r"^[A-Za-z0-9]+$")

    class Config:
        extra = "forbid"

