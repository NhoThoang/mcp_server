from pydantic import BaseModel

class Question(BaseModel):
    user_id: str
    question: str

class AnswerOut(BaseModel):
    answer: str
    cached: bool
