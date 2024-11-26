import asyncio
import json
from openaiService import OpenAIService
from aidevs import Aidevs
import os

openai_service = OpenAIService()
aidevs_service = Aidevs()

def read_lab_files():
    base_path = r"D:/Ignacy/Code/AI/Resources/lab_data/"
    files = {
        "correct": "correct.txt",
        "incorrect": "incorrect.txt",
        "verify": "verify.txt"
    }
    
    file_contents = {}
    
    for key, filename in files.items():
        file_path = os.path.join(base_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                file_contents[key] = file.read()
        except FileNotFoundError:
            print(f"Warning: File {filename} not found")
        except Exception as e:
            print(f"Error reading {filename}: {str(e)}")
            
    return file_contents


def split_file_to_lines(file_content):
   if not file_content:
       return []
   
   # Dzieli tekst na linie i usuwa białe znaki z początku i końca każdej linii
   lines = [line.strip() for line in file_content.split('\n')]
   # Usuwa puste linie
   lines = [line for line in lines if line]
   
   return lines

# Przykład użycia:
files = read_lab_files()
verify_lines = split_file_to_lines(files.get('verify'))
correct_lines = split_file_to_lines(files.get('correct'))
incorrect_lines = split_file_to_lines(files.get('incorrect'))


def jsonl(line: str, correct: bool):
    return {
        "messages": [
            {"role": "system", "content": "Decide if array of numbers is correct."},
            {"role": "user", "content": line},
            {"role": "assistant", "content": "correct" if correct else "incorrect"}
        ]
    }

def create_jsonl():
    jsonl_data = []
    for line in correct_lines:
        jsonl_data.append(jsonl(line, True))
    for line in incorrect_lines:
        jsonl_data.append(jsonl(line, False))
    return jsonl_data
 
def save_jsonl(jsonl_data):

    with open("jsonl_data.jsonl", "w") as file:
        for item in jsonl_data:
            json.dump(item, file)
            file.write("\n")
            
async def fine_tuned_completion(line: str):
    response = await openai_service.completion(
        model="ft:gpt-4o-mini-2024-07-18:personal:aidevss04e02-v1:AXu7SIeL",
        messages=[
            {
                "role": "system",
                "content": "Decide if array of numbers is correct."
            },
            {
                "role": "user",
                "content": line
            }
        ]
    )
    return response.choices[0].message.content

async def main():
    for line in verify_lines:
        line_split = line.split("=")
        response = await fine_tuned_completion(line_split[1])
        print(line_split[0], response)

async def asdf():
    answer = ["01", "02", "10"]
    result = await aidevs_service.verify("research", answer)
    print(result)

asyncio.run(asdf())
