from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from mcp_Server.core.config import config_env_manager as config
qdrant = QdrantClient(
    host=config.QDRANT_HOST,
    port=config.QDRANT_PORT
)

async def init_qdrant():
    try:
        qdrant.get_collection("qa")
    except:
        qdrant.recreate_collection(
            collection_name="qa",
            vectors_config=VectorParams(size=128, distance=Distance.COSINE)
        )
        print("Qdrant collection 'qa' created successfully.")
    else:
        print("Qdrant collection 'qa' already exists.")