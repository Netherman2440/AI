import asyncio
import os

from openaiService import OpenAIService
from aidevs import Aidevs

answers = {
    '01': "Podczas pierwszej próby transmisji materii w czasie użyto truskawki.",
    '02': "Testowa fotografia została wykonana na rynku w Krakowie.",
    '03': "Rafał Bomba chciał znaleźć hotel w Grudziądzu.",
    '04': "Rafał Bomba pozostawił resztki ciasta z ananasem.",
    '05': "Nazwa BNW w nowym modelu językowym jest akronimem od „Brave New World” – „Nowy Wspaniały Świat”.",
}

async def main():
    openai = OpenAIService()
    devs = Aidevs()
    answer = await devs.get("https://centrala.ag3nts.org/data/KLUCZ-API/arxiv.txt", False)
    print(answer)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    article_path = os.path.join(script_dir, 'article.md')
    
    with open(article_path, 'r', encoding='utf-8') as file:
        article = file.read()

    links_path = os.path.join(script_dir, 'links.md')
    
    with open(links_path, 'r', encoding='utf-8') as file:
        links = file.read()

    response = await openai.completion([{
        "role": "system",
        "content": f'''
        Your task is to answer user question about the article. Question might be about text, image or audio. 

        Article:
        {article}

        '''
    },
    {
            "role": "user",
            "content": "Od czego pochodzą litery BNW w nazwie nowego modelu językowego?"
        }])

    print(response)

async def answer_question():
    devs = Aidevs()
    answer = await devs.verify('arxiv',answers)
    print(answer)

if __name__ == "__main__":
    asyncio.run(answer_question())
