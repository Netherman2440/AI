

from typing import Any, Dict

import requests

async def post(url: str, data: Dict[str, Any], api_key: str) -> Dict[str, Any]:

    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.post(url, data=data, headers=headers)
    print(response.json())
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
