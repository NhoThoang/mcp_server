# services/history_service.py
from mcp_Server.models.mongo_history import History

async def save(user_id: str, question: str, answer: str):
    history = History(user_id=user_id, question=question, answer=answer)
    await history.insert()


# async def save(user_id: str, question: str, answer: str):
#     await collection_history.insert_one({"user_id": user_id, "question": question, "answer": answer})