from fastapi import HTTPException
from pydantic import BaseModel, ValidationError
from typing import Type

def validate_and_create_response(response_data: dict, response_model: Type[BaseModel]) -> BaseModel:
    """
    Generic helper function to validate response data and create a Pydantic model object.

    Args:
        response_data (dict): The data to validate.
        response_model (Type[BaseModel]): The Pydantic model to validate against.

    Returns:
        BaseModel: An instance of the validated Pydantic model.

    Raises:
        HTTPException: If validation fails, raises a 500 error with details.
    """
    try:
        return response_model(**response_data)
    except ValidationError as e:
        raise HTTPException(status_code=500, detail=f"Response validation error: {e}")