from fastapi import APIRouter
from mcp_Server.schemas.qa import Question
from mcp_Server.services.ask_service import handle_question

router = APIRouter()

@router.post("/ask")
async def ask(data: Question):
    return await handle_question(data.user_id, data.question)