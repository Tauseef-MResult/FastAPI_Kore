from app.db.db_connection import counters_collection

def get_idea_id():
    counter = counters_collection.find_one_and_update(
                {"_id": "idea_id"},
                {"$inc": {"sequence_value": 1}},
                return_document=True,
                upsert=True
            )

    idea_id = f"IDEA_{counter['sequence_value']}"
    return idea_id