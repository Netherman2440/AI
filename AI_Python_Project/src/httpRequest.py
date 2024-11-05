from typing import Any, Dict

import requests
import json

async def post(url: str, data: str, api_key: str = None) -> Dict[str, Any]:
    headers = {
        'Content-Type': 'application/json'
    }
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'



    response = requests.post(url, data=data, headers=headers)
    return response.json()

async def get(url: str, api_key: str = None) -> Dict[str, Any]:
    
    if api_key:
        headers = {
            'Authorization': f'Bearer {api_key}'
        }
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url)
    return response.json()
