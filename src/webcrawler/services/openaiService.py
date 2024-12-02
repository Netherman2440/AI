import base64
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
        
        stream: bool = False
    ):
   
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            
        response_format= { "type": "json_object" } if jsonMode else { "type": "text" },
        stream=stream
        )
        return response

    async def audio_transcription(self, file_path: str):
        audio_file = open(file_path, "rb")
        response = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return response.text
    
    

    async def vision(
            self, 
            file_path_or_url: str,
            model: str = "gpt-4o",
            jsonMode: bool = False,
            max_tokens: int = 300,
            stream: bool = False
        ):
        # Determine if input is URL or file path
        is_url = file_path_or_url.startswith(('http://', 'https://'))
        
        if is_url:
            image_url = file_path_or_url
        else:
            # Handle local file
            image_data = open(file_path_or_url, "rb").read()
            base64_image = base64.b64encode(image_data).decode("utf-8")
            image_url = f"data:image/jpeg;base64,{base64_image}"

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Describe this image in detail.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            },
                        },
                    ],
                },
            ],
            response_format= { "type": "json_object" } if jsonMode else { "type": "text" },
            max_tokens=max_tokens,
            stream=stream
        )
        return response.choices[0].message.content

    async def create_embedding(self, input: str, model: str = "text-embedding-3-large"):
        response = self.client.embeddings.create(
            model=model,
            input=input,
            encoding_format="float",
            
        )
        return response.data[0].embedding

    


# TODO:

# - add jina embedding
# - add function to count tokens in messages
# - add function to get tokenizer
