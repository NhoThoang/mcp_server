# Demo: Kiến trúc MCP server dùng FastAPI + MongoDB + Qdrant + Redis

from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import hashlib
import uuid

# MongoDB (chat history)
from motor.motor_asyncio import AsyncIOMotorClient

# Qdrant (vector search)
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

# Redis (cache Q&A)
import redis.asyncio as redis

app = FastAPI()

# --- Init connections ---
mongo = AsyncIOMotorClient("mongodb://localhost:27017")
db = mongo["mcp"]
collection_history = db["chat_logs"]

qdrant = QdrantClient(host="localhost", port=6333)
redis_cache = redis.Redis(host="localhost", port=6379, decode_responses=True)

# --- Define Models ---
class Question(BaseModel):
    user_id: str
    question: str

# --- Fake embedding function ---
def embed_text(text: str):
    return [float((int(hashlib.sha256(text.encode()).hexdigest(), 16) % 1000) / 1000.0)] * 128

# --- API: Gửi câu hỏi ---
@app.post("/ask")
async def ask_question(data: Question):
    key = f"cache:{data.user_id}:{data.question}"
    cached = await redis_cache.get(key)
    if cached:
        return {"answer": cached, "cached": True}

    # search in vector db (qdrant)
    vector = embed_text(data.question)
    search_result = qdrant.search(collection_name="qa", query_vector=vector, top=1)
    if search_result and search_result[0].score > 0.9:
        answer = search_result[0].payload["answer"]
    else:
        answer = f"(GPT response) Trả lời giả lập cho: {data.question}"
        qdrant.upsert(collection_name="qa", points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"question": data.question, "answer": answer}
            )
        ])

    await redis_cache.set(key, answer, ex=3600)
    await collection_history.insert_one({"user_id": data.user_id, "question": data.question, "answer": answer})
    return {"answer": answer, "cached": False}

# --- Init Qdrant Collection (run once) ---
@app.on_event("startup")
async def init_qdrant():
    try:
        qdrant.get_collection("qa")
    except:
        qdrant.recreate_collection(
            collection_name="qa",
            vectors_config=VectorParams(size=128, distance=Distance.COSINE)
        )
