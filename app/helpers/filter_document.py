
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


def filter_idea_document(idea):
    filtered_idea_document = {
                "idea_id": idea["idea_id"],
                "employee_id": idea["employee_id"],
                "title": idea["title"],
                "description": idea["description"],
                "category": idea["category"],
                "impact": idea["impact"],
                "submission_date": idea["submission_date"],
                "status": idea["status"],
                "evaluation_score": idea["evaluation_score"],
                "comments": idea["comments"]
            }
    return filtered_idea_document


def filter_idea_documents_list(ideas):
    filtered_ideas = []
    for idea in ideas:
        filtered_idea = filter_idea_document(idea)
        filtered_ideas.append(filtered_idea)
    return filtered_ideas