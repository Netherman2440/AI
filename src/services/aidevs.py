import httpx


async def verify(self, task_id: str, answer: str | dict | list, is_json: bool = True):
    url = 'https://centrala.ag3nts.org/report'

    # Tworzymy payload bez modyfikowania answer
    payload = {
        "task": task_id,
        "apikey": self.api_key,
        "answer": answer  # answer pozostaje w oryginalnej formie
    }

    headers = {
        'Content-Type': 'application/json'
    }   

    async with httpx.AsyncClient() as client:
        print(f"POST {url}")
        print(f"Headers: {headers}")
        print(f"Data: {payload}")
        response = await client.post(url, json=payload, headers=headers)
        return response.json() if is_json else response.text 