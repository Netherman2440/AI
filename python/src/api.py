from flask import Flask, request, jsonify
# Dodaj gunicorn do wymagań
import os

app = Flask(__name__)

@app.route('/api/data', methods=['POST'])
def handle_post():
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({"error": "Brak danych"}), 400
    


    
    response = {
        "status": "success",
        "message": "Dane otrzymane pomyślnie",
        "received_data": data,
        "description": "Opis danych"
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
