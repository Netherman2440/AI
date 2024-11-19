from typing import TypedDict
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams
import os
from dotenv import load_dotenv
from openaiService import OpenAIService
import json
import os

load_dotenv()

class Point(TypedDict, total=False):
    id: str | None
    text: str
    metadata: dict[str, any] | None
    vector: list[float]

class VectorService:
    def __init__(self):
        self.client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))
        self.openai = OpenAIService()

    def ensure_collection(self, collection_name: str):
        collections = self.client.get_collections()
        if not any(collection.name == collection_name for collection in collections.collections):
            self.client.create_collection(
                collection_name, 
                vectors_config=VectorParams(size=1024, distance="Cosine")
            )


    async def initialize_collection_with_data(self, collection_name: str, points: list[Point]):
        self.ensure_collection(collection_name)
        await self.add_points(collection_name, points)


    async def add_points(self, collection_name: str, points: list[Point]):
        points_to_upsert = []
        for point in points:
            embeddings = await self.openai.create_embedding(point["text"])
            points_to_upsert.append({
                "id": point.get("id", str(uuid.uuid4())),
                "vector": embeddings,
                "payload": {
                    "text": point["text"],
                    **(point.get("metadata", {}))
                }
            })

        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        points_file = os.path.join(current_dir, 'points.json')

        # Write points to JSON file
        with open(points_file, 'w', encoding='utf-8') as f:
            json.dump(points_to_upsert, f, indent=4, ensure_ascii=False)

        self.client.upsert(collection_name, points_to_upsert)


    async def search(self, collection_name: str, query: str, filter: dict[str, any] = None, limit: int = 10):
        emb_query = await self.openai.create_embedding(query)

        response = self.client.search(collection_name, emb_query, query_filter=filter, limit=limit)
        return response
    

    