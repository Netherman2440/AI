import os
from typing import Any, Dict

import dotenv
import requests
import json

async def post(url: str, data: str, api_key: str = None) -> Dict[str, Any]:
    headers = {
        'Content-Type': 'application/json'
    }
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'



    response = requests.post(url, data=data, headers=headers)
    return response.text

async def get(url: str, api_key: str = None) -> Dict[str, Any]:
    
    if api_key:
        headers = {
            'Authorization': f'Bearer {api_key}'
        }
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url)
    return response.text

async def verify(task: str, answer: str) -> str:
    url = 'https://centrala.ag3nts.org/report'
    dotenv.load_dotenv()
    api_key = os.getenv('AIDEVS_API_KEY')
    data = json.dumps({
        "task": task,
        "apikey": api_key,
        "answer": answer
    })

    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, data=data, headers=headers)
    return response.json()  # lub response.text() jeśli odpowiedź nie jest w JSON
