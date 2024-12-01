from openaiService import OpenAIService
from aidevs import Aidevs
import asyncio

openaiService = OpenAIService()
aidevs = Aidevs()

async def main():
    response =  await aidevs.get("https://centrala.ag3nts.org/data/TUTAJ-KLUCZ/softo.json")

    print(response)

if __name__ == "__main__":
    asyncio.run(main())


