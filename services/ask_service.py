from mcp_Server.core.vector_utils import embed_text
from mcp_Server.crud import qa, chat_history
from mcp_Server.db.redis_cache import get_cache, set_cache

async def handle_question(user_id: str, question: str):
    key = f"cache:{user_id}:{question}"
    cached = await get_cache(key)
    if cached:
        return {"answer": cached, "cached": True}

    vector = embed_text(question)
    hit = qa.search_similar(vector)
    if hit:
        answer = hit
    else:
        answer = f"(GPT giả lập) Trả lời cho: {question}"
        # qa.upsert_question_answer(question, answer, vector)
        qa.upsert_question_answer(question, answer, vector)

    await set_cache(key, answer)
    await chat_history.save(user_id, question, answer)
    return {"answer": answer, "cached": False}
