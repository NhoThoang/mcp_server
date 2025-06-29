import redis.asyncio as redis
from mcp_Server.core.config import config_env_manager as config


redis_client = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    password=config.REDIS_PASSWORD if config.REDIS_PASSWORD else None,
    decode_responses=True  # Ensure strings are returned as strings
)

async def get_cache(key: str):
    return await redis_client.get(key)

async def set_cache(key: str, value: str, ex: int = 3600):
    await redis_client.set(key, value, ex=ex)