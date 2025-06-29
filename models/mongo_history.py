# models/history.py
from beanie import Document
from pydantic import BaseModel
from datetime import datetime

class History(Document):
    user_id: str
    question: str
    answer: str
    created_at: datetime = datetime.utcnow()
    