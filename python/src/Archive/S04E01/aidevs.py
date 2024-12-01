
import json
import os
import dotenv
import httpx
import requests

dotenv.load_dotenv()

class Aidevs:
    def __init__(self):
        self.api_key = os.getenv("AIDEVS_API_KEY")
    
    async def get(self, url: str, is_json: bool = True):

        
        if "KLUCZ-API" in url:
            url = url.replace("KLUCZ-API", self.api_key)
        elif "KLUCZ" in url:
            url = url.replace("KLUCZ", self.api_key)

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json() if is_json else response.text
        
    async def verify(self, task_id: str, answer: object, is_json: bool = True):
        url = 'https://centrala.ag3nts.org/report'


        data = json.dumps({
            "task": task_id,
            "apikey": self.api_key,
            "answer": answer
        })

        headers = {
            'Content-Type': 'application/json'
        }   

        async with httpx.AsyncClient() as client:
            print(f"POST {url}")
            print(f"Headers: {headers}")
            print(f"Data: {data}")
            response = await client.post(url, data=data, headers=headers)
            return response.json() if is_json else response.text
    
    async def api(self, query: str):
        url = 'https://centrala.ag3nts.org/report'
        data = json.dumps({
            "task": "photos",
            "apikey": self.api_key,
            "answer": query
        })

        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data)
            return response


