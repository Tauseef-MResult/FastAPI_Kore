from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Optional
from pydantic import ValidationError
from app.db.db_connection import ideas_collection, users_collection, evaluations_collection
from app.schemas.idea_schema import IdeaBase, IdeaResponse
from app.schemas.evaluation_schema import EvaluationBase, EvaluationResponse
from app.services.email_service import send_idea_submission_email, send_evaluation_notification
from app.helpers.filter_document import filter_idea_document, filter_idea_documents_list
from app.helpers.response_validator import validate_and_create_response
from app.helpers.idea_id_generator import idea_id


router = APIRouter()


@router.post("/submit_idea", response_model=IdeaResponse)
async def submit_idea(idea: IdeaBase):
    try:
        # Check if the user exists
        user = users_collection.find_one({"employee_id": idea.employee_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if the user is an admin
        if user["user_type"] == "admin":
            raise HTTPException(status_code=403, detail="Admin users are not allowed to submit ideas")

        # Check if the user has already submitted an idea with the same title
        existing_idea = ideas_collection.find_one({"employee_id": idea.employee_id, "title": idea.title, "category": idea.category})
        if existing_idea:
            raise HTTPException(status_code=400, detail="User has already submitted this idea before")

        # Prepare the idea document
        idea_dict = idea.dict()
        idea_dict["idea_id"] = idea_id
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
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to insert idea details into the database")


        # Send email notification to the user
        if not send_idea_submission_email(email=user["email"],name=user["name"],idea_id=idea_id,
            title = idea_dict["title"],category=idea_dict["category"]):
            raise HTTPException(status_code=500, detail="Failed to send submission email")

        response_data = {"idea_id": idea_id, **idea_dict_copy}
        return validate_and_create_response(response_data, IdeaResponse)

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
        if not ideas:
            raise HTTPException(status_code=404, detail="User hasn't submitted any ideas")

        # Convert MongoDB documents to IdeaResponse schema
        filtered_ideas = filter_idea_documents_list(ideas)

        return filtered_ideas

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")



@router.get("/get_all_ideas", response_model=list[IdeaResponse])
async def get_all_ideas(category: Optional[str] = None, status: Optional[str] = None):
    try:
        # Build query dictionary based on provided parameters
        query = {}
        if category:
            query["category"] = category
        if status:
            query["status"] = status

        # Fetch all ideas from the database
        ideas = list(ideas_collection.find(query))
        if not ideas:
            raise HTTPException(status_code=404, detail="No ideas submitted")

        # Convert MongoDB documents to IdeaResponse schema
        filtered_ideas = filter_idea_documents_list(ideas)

        return filtered_ideas

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


def validate_and_create_evaluation_response(response_data: dict) -> EvaluationResponse:
    """Helper function to validate response data and create an EvaluationResponse object."""
    try:
        return EvaluationResponse(**response_data)
    except ValidationError as e:
        raise HTTPException(status_code=500, detail=f"Response validation error: {e}")

@router.post("/evaluate_idea", response_model=EvaluationResponse)
async def evaluate_idea(evaluation: EvaluationBase):
    try:

        # Check if idea exists
        idea = ideas_collection.find_one({"idea_id": evaluation.idea_id})
        if not idea:
            raise HTTPException(status_code=404, detail="Idea not found")

        # Check if idea has been evaluated before
        idea_evaluated = evaluations_collection.find_one({"idea_id": evaluation.idea_id})
        if idea_evaluated :
            raise HTTPException(status_code=404, detail="Idea has been already evaluated before")

        #Check if evaluator id/admin id is valid
        admin = users_collection.find_one({"employee_id": evaluation.evaluator_id, "user_type": "admin"})
        if not admin:
            raise HTTPException(status_code=404, detail="Invalid evaluator ID")


        # Calculate the evaluation score
        evaluation_score = evaluation.feasibility_score + evaluation.impact_score + evaluation.resource_score

        # Prepare the evaluation document
        evaluation_dict = evaluation.dict()
        evaluation_dict["evaluation_score"] = evaluation_score
        evaluation_dict["evaluation_date"] = datetime.now()

        evaluation_dict_copy = evaluation_dict.copy()

        # Insert the evaluation into the database
        result = evaluations_collection.insert_one(evaluation_dict)
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to insert evaluation details into the database")

        # Update the idea with evaluation details
        update_result = ideas_collection.update_one(
            {"idea_id": evaluation.idea_id},
            {
                "$set": {
                    "evaluation_score": evaluation_score,
                    "status": evaluation.status,
                    "comments": evaluation.comments
                }
            }
        )

        if not update_result:
            raise HTTPException(status_code=404, detail="Failed to update user ideas table")

        # Fetch the idea and user details for email notification
        user = users_collection.find_one({"employee_id": idea["employee_id"]})

        # Send email notification to the user
        if not send_evaluation_notification(email=user["email"], name=user["name"], idea_title=idea["title"],
                                idea_category=idea["category"], status=evaluation.status, comments=evaluation.comments ):
            raise HTTPException(status_code=500, detail="Failed to send evaluation notification email")

        response_data = {"evaluation_id": str(result.inserted_id), **evaluation_dict_copy}
        return validate_and_create_response(response_data, EvaluationResponse)

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")