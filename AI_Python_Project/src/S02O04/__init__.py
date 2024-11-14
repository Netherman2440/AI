from aidevs import Aidevs
from openaiService import OpenAIService
import asyncio

aidevs = Aidevs()
openai = OpenAIService()

async def main():
    response = await aidevs.get('https://centrala.ag3nts.org/data/KLUCZ/cenzura.txt', is_json=False)
    print(response)

    response = await openai.completion(
        messages=[
            {"role": "system", "content": "Your task is to count the number of words in the text."},
            {"role": "user", "content": response}
        ]
    )
    print(response.choices[0].message.content)
if __name__ == "__main__":
    asyncio.run(main())