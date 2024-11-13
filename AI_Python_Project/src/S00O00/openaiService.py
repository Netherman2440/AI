import os
import dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
class OpenAIService:
    def __init__(self):
        dotenv.load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)


    async def completion(
        self,
        messages: list[ChatCompletionMessageParam],
        model: str = "gpt-4o",
        jsonMode: bool = False,
        max_tokens: int = 300,
        stream: bool = False
    ):
   
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
        response_format= { "type": "json_object" } if jsonMode else { "type": "text" },
        stream=stream
        )
        return response
'''
    async def createEmbedding(self, input: str | list[str]):
        response = self.client.embeddings.create(
            model="text-embedding-3-large",
            input=input,
            encoding_format="float"
        )
        return response.data[0].embedding
'''

# TODO:

# - add function to count tokens in messages
# - add function to get tokenizer
