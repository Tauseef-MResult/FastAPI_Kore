from fastapi import APIRouter, HTTPException
from app.db.db_connection import users_collection
from app.schemas.user_schema import UserBase, UserResponse, AuthRequest
from app.services.password_service import generate_password, encrypt_password, decrypt_password
from app.services.email_service import send_email
from app.helpers.filter_document import filter_user_document


router = APIRouter()

@router.post("/add_user", response_model=UserResponse)
async def add_user(user: UserBase):
    try:
        # Check if user already exists
        if users_collection.find_one({"employee_id": user.employee_id}) or users_collection.find_one({"email": user.email}):
            raise HTTPException(status_code=400, detail="Employee already exists in records")

        # Insert user into database
        user_dict = user.dict()
        password = generate_password()
        user_dict["password"] = encrypt_password(password)
        result = users_collection.insert_one(user_dict)

        if not send_email(user.email, user.name, password):
            raise HTTPException(status_code=500, detail="Failed to send email")

        return {"id": str(result.inserted_id), **user.dict()}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")



@router.get("/get_user_details/{employee_id}", response_model=UserResponse)
async def get_user_details(employee_id: str):
    try:
        user = users_collection.find_one({"employee_id": employee_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return filter_user_document(user)

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")



@router.post("/authenticate_user")
async def authenticate_user(auth_data: AuthRequest):
    try:
        user = users_collection.find_one({"employee_id": auth_data.employee_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Verify password
        if not decrypt_password(user["password"], auth_data.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return {"message": "User authenticated successfully"}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")



@router.delete("/delete_user/{employee_id}")
async def delete_user(employee_id: str):
    try:
        result = users_collection.delete_one({"employee_id": employee_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
