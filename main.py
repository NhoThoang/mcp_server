# --- app/main.py ---
from fastapi import FastAPI
from mcp_Server.api.routes_ask import router as ask_router
from mcp_Server.db.qdrant import init_qdrant
from mcp_Server.db.mongo import init_db
from mcp_Server.core.middlewares import setup_middlewares

app = FastAPI()
setup_middlewares(app)

app.include_router(ask_router, prefix="/api")

@app.on_event("startup")
async def on_startup():
    await init_qdrant()
@app.on_event("startup")
async def startup_event():
    await init_db()
