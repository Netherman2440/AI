import asyncio
import os

from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from httpRequest import get, post
from chatBot import ChatBot
from dataclasses import dataclass, asdict
from typing import Optional
import json

post_url = "https://centrala.ag3nts.org/report" 

load_dotenv()
api_key = os.getenv("AIDEVS_API_KEY")    

json_url = f'https://centrala.ag3nts.org/data/{api_key}/json.txt'


@dataclass
class TestData:
    q: str
    a: str

@dataclass
class QuestionData:
    question: str
    answer: int
    test: Optional[TestData] = None

def evaluate_expression(expression: str) -> int:
    # Rozdziel string na liczby
    num1, num2 = map(int, expression.split('+'))
    return num1 + num2


async def main():
    
    json_data = await get(json_url)
    # Parsowanie JSON do listy obiektów QuestionData
    parsed_data = []
    for item in json_data["test-data"]:
        # Sprawdź czy wynik działania jest poprawny
        correct_answer = evaluate_expression(item["question"])
        if correct_answer != item["answer"]:
            print(f"Znaleziono błąd w działaniu {item['question']}: {item['answer']} -> {correct_answer}")
            item["answer"] = correct_answer
        
        test_data = None
        if "test" in item:
            test_data = TestData(
                q=item["test"]["q"],
                a=item["test"]["a"]
            )
        
        question_data = QuestionData(
            question=item["question"],
            answer=item["answer"],
            test=test_data
        )
        parsed_data.append(question_data)
        
    
    chatbot = ChatBot()
    chatbot.system_prompt = """
    You are a helpful assistant that can answer questions about the given JSON data.
"""
    for question_data in parsed_data:
        if question_data.test:
            answer = await chatbot.ask(question_data.test.q)
            print(question_data.test.q, answer)
            question_data.test.a = answer

    json_data = format_json_data(parsed_data)
    
    # Convert string to JSON object
    json_data = json.loads(json_data)

    final_answer = {
    "task": "JSON",
    "apikey": api_key,
    "answer": json_data
}
    # Wyślij przetworzone dane
    print(json.dumps(final_answer))

    
    response = await post(post_url, json.dumps(final_answer))
    print(response)

def format_json_data(parsed_data):

    json_string = f'{{"apikey": "{api_key}",\n' + \
    """
    "description": "This is simple calibration data used for testing purposes. Do not use it in production environment!",
    "copyright": "Copyright (C) 2238 by BanAN Technologies Inc.",
    "test-data": [
        """
    
    
    for i, item in enumerate(parsed_data):
        json_string += "{"
        json_string += f'"question": "{item.question}",'
        
        if item.test is None:
            json_string += f'"answer": {item.answer}'
            json_string += '}'
        else:
            json_string += f'"answer": {item.answer},'
            json_string += '"test": {'
            json_string += f'"q": "{item.test.q}",'
            json_string += f'"a": "{item.test.a}"'
            json_string += '}'
            json_string += '}'
        
        if i < len(parsed_data) - 1:
            json_string += ','
    
    json_string += "]}"
    return json_string

if __name__ == "__main__":
    asyncio.run(main())
    