
import asyncio
import os
import dotenv
from chatBot import ChatBot

from httpRequest import get, verify


dotenv.load_dotenv()
aidevs_api_key = os.getenv("AIDEVS_API_KEY")

get_url = f'https://centrala.ag3nts.org/data/{aidevs_api_key}/cenzura.txt'

print(get_url)

chatBot = ChatBot()

async def main():
    response = await get(get_url)
    print(response)
    chatBot.system_prompt = '''
    You are a helpful assistant that can answer questions about the text.
    '''
    message = f'''
    Oto tekst do ocenzurowania:
    {response}

   Zamień wszelkie wrażliwe dane (imię + nazwisko, nazwę ulicy + numer, miasto, wiek osoby na słowo CENZURA.

   
     Example:
                        user: Tożsamość osoby: Jan Kowalski. Zamieszkały w Gdańsku przy ul. Głównej 2. Ma 43 lata.
                        assistant <answer>Tożsamość osoby: CENZURA. Zamieszkały w CENZURA przy ul. CENZURA. Ma CENZURA lata.</answer>
    '''
    answer = await chatBot.ask(message)
    print(answer)


    result = await verify('CENZURA', answer)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())