from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.db.db_connection import ideas_collection, users_collection
from app.schemas.idea_schema import IdeaBase, IdeaResponse
from app.services.email_service import send_idea_submission_email
from app.helpers.filter_document import filter_idea_document

router = APIRouter()

@router.post("/submit_idea", response_model=IdeaResponse)
async def submit_idea(idea: IdeaBase):
    try:
        # Check if the user exists
        user = users_collection.find_one({"employee_id": idea.employee_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Prepare the idea document
        idea_dict = idea.dict()
        idea_dict["submission_date"] = datetime.now()
        idea_dict["status"] = "Under Review"
        idea_dict["evaluation_score"] = 0.0
        idea_dict["comments"] = "NA"

        """
        MongoDB driver automatically adds the _id field to the dictionary you pass to insert_one(), 
        which was causing problems with Pydantic Response validation - hence I create shallow copy of response dict
        """
        idea_dict_copy = idea_dict.copy()

        # Insert the idea into the database
        result = ideas_collection.insert_one(idea_dict) # Here _id gets auto added to idea_dict
        idea_id = str(result.inserted_id)


        # Send email notification to the user
        if not send_idea_submission_email(
            email=user["email"],
            name=user["name"],
            idea_id=idea_id,
            title=idea_dict["title"],
            category=idea_dict["category"]
        ):
            raise HTTPException(status_code=500, detail="Failed to send submission email")
        return {"idea_id": idea_id, **idea_dict_copy}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")



@router.get("/get_user_ideas/{employee_id}", response_model=list[IdeaResponse])
async def get_user_ideas(employee_id: str):
    try:
        # Check if the user exists
        user = users_collection.find_one({"employee_id": employee_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Fetch all ideas submitted by the user
        ideas = list(ideas_collection.find({"employee_id": employee_id}))

        # Convert MongoDB documents to IdeaResponse schema
        filtered_ideas = []
        for idea in ideas:
            filtered_idea = filter_idea_document(idea)
            filtered_ideas.append(filtered_idea)

        return filtered_ideas

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")