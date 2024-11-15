import asyncio
import os
import re
import aiohttp

import dotenv
import requests
import json

import AI_Python_Project.src.ChatBot as ChatBot

dotenv.load_dotenv()

#first we need to log to firecrawl 



fs_api_key = os.getenv("FIRECRAWL_API_KEY")
aidevs_api_key = os.getenv("AIDEVS_API_KEY")

fc_url = "https://api.firecrawl.dev/v1/scrape"

ai_url = "https://xyz.ag3nts.org/"

payload = {
    "url": ai_url,
    "formats": ["markdown"],
    "onlyMainContent": True,
    "headers": {},
}

headers = {
    "Authorization": f"Bearer {fs_api_key}",
    "Content-Type": "application/json"
}


response = requests.request("POST", fc_url, json=payload, headers=headers)
print(f"Response: {response.text}")
# Zamiast używać przykładowego tekstu, użyjmy faktycznej odpowiedzi z API
response_json = json.loads(response.text)

print(f"Response JSON: {response_json}")

print("JSON structure:", response_json.keys())
markdown_content = response_json['data']['markdown']

#scrap the website: https://xyz.ag3nts.org

print(markdown_content)
pass
# Wyodrębnienie pytania
question_start = markdown_content.find('Question:')
login_start = markdown_content.find('Login')

if question_start != -1 and login_start != -1:
    # Bierzemy tekst między "Question:" a "Login", pomijając puste linie
    question_text = markdown_content[question_start:login_start]
    # Usuwamy "Question:" i czyścimy tekst z pustych linii
    question = question_text.replace('Question:', '').strip()
    print(f"Wyodrębnione pytanie: {question}")
else:
    print("Nie znaleziono pytania w tekście")


#show the results (Login, password and question)
login = 'tester'
password = '574e112a'
# ask gpt with a question from the results
chatbot = ChatBot.ChatBot()

async def get_ai_answer(question: str):
    chatbot.add_system_prompt("Return just numbers.")
    answer = await chatbot.askAI(question)
    return answer


# get the answer from gpt
answer = asyncio.run(get_ai_answer(question))
answer_int = int(answer)
print(answer_int)

# send the answer to the website (login, password and answer)



data = {
    'username': login,
    'password': password,
    'answer': answer
}


# Wysyłamy POST request
response = requests.post(ai_url, data=data)


print(response.status_code)
print(response.text)


flag_match = re.search(r'{{FLG:(.*?)}}', response.text)

if flag_match:
    flag = flag_match.group(1)
    print(flag)
else:
    print("No flag found")

