import asyncio
import json
from flask import Flask, request, jsonify
from prompt import prompt
from openaiService import OpenAIService
import os


app = Flask(__name__)
openaiService = OpenAIService()

@app.route('/api/data', methods=['POST'])
def handle_post():
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({"error": "Brak danych"}), 400
    

    
    response = asyncio.run(openaiService.completion(
        messages=[
            {"role": "system", "content": prompt()},
            {"role": "user", "content": data["instruction"]}
        ]
    ))
    print(response.choices[0].message.content)


    answer = response.choices[0].message.content
    if answer.startswith("```json"):
        answer = answer.replace("```json", "").replace("```", "")
    answer = json.loads(answer)["answer"]
    print(answer)
    response = {
        "status": "success",
        "message": "Dane otrzymane pomyślnie",
        "received_data": data,
        "description": answer
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
