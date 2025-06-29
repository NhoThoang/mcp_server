from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid

qdrant = QdrantClient(host="localhost", port=6333)

COLLECTION = "qa"

def search_similar(vector):
    res = qdrant.search(collection_name=COLLECTION, query_vector=vector, limit=1)
    if res and res[0].score > 0.9:
        return res[0].payload["answer"]
    return None

def upsert_qa(question, answer, vector):
    qdrant.upsert(collection_name=COLLECTION, points=[
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={"question": question, "answer": answer}
        )
    ])
def upsert_question_answer(question, answer, vector):
    """
    Upsert a question-answer pair into the Qdrant collection.
    """
    upsert_qa(question, answer, vector)
    return {"status": "success", "message": "Question and answer upserted successfully."}
