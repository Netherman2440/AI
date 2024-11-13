import asyncio
import dotenv

import os

from openai import OpenAI
import requests


async def main():
    dotenv.load_dotenv()
    api_key = os.getenv("AIDEVS_API_KEY")
    photo_desc_url = f'https://centrala.ag3nts.org/data/{api_key}/robotid.json'
    response = requests.get(photo_desc_url)
    answer = response.json()
    print(answer)
    message = answer['description']
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response =  client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "Your task is convert user message to description of photo. This has to be a prompt for DALL-E 3. "}, {"role": "user", "content": message}]
    )
    print(response.choices[0].message.content)
   
if(__name__ == "__main__"):
    asyncio.run(main())
