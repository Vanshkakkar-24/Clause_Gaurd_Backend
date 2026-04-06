from app.history import history_collection
from datetime import datetime


def save_contract_history(
    user_id: str,
    file_name: str,
    type: str,
    result: dict
):

    history_collection.insert_one({

        "user_id": user_id,

        "file_name": file_name,

        "type": type,

        "result": result,

        "created_at": datetime.utcnow()

    })