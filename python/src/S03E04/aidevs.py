
import json
import os
import dotenv
import httpx
import requests

dotenv.load_dotenv()

class Aidevs:
    def __init__(self):
        self.api_key = os.getenv("AIDEVS_API_KEY")
    
    async def people(self, query: str):
        url = 'https://centrala.ag3nts.org/people'
        return await self.query(url, query)
    
    async def places(self, query: str):
        url = 'https://centrala.ag3nts.org/places'
        return await self.query(url, query)

    async def query(self, url: str, query: str):

        data = json.dumps({
            "apikey": self.api_key,
            "query": query
        })

        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data)
            return response
        
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
        
    

    


