import asyncio
from vectorservice import VectorService, Point
from openaiService import OpenAIService

vector_service = VectorService()

points : list[Point] = [
    {"text": "Alicja jest moją żoną"},
    {"text": "Lilianna jest moją córką"},
    {"text": "Jestem programistą"},
    {"text": "Pracuję w Pythonie i w C#"}
]

print(asyncio.run(vector_service.search("test", "rodzina")))

