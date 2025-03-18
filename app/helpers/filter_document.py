
# Convert MongoDB User document to UserResponse schema
def filter_user_document(user):
    filtered_user_document = {
        "id": str(user["_id"]),  # Convert ObjectId to string
        "employee_id": user["employee_id"],
        "name": user["name"],
        "email": user["email"],
        "user_type": user["user_type"]
    }
    return filtered_user_document