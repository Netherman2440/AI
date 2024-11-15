from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Konfiguracja limitera
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["1 per 10 seconds"]
)

# Przykładowa baza danych jako lista słowników
database = [
    {"id": 1, "name": "Quest A", "status": "completed"},
    {"id": 2, "name": "Quest B", "status": "in-progress"}
]

# Endpoint główny
@app.route("/")
def home():
    return "Hello, World!"

# Endpoint, który zwraca wszystkie dane z bazy
@app.route("/quests", methods=["GET"])
@limiter.limit("1 per 10 seconds")
def get_all_quests():
    return jsonify(database)

# Endpoint, który zwraca dane konkretnego elementu (np. questa) na podstawie jego ID
@app.route("/quests/<int:quest_id>", methods=["GET"])
@limiter.limit("1 per 10 seconds")
def get_quest(quest_id):
    quest = next((q for q in database if q["id"] == quest_id), None)
    if quest:
        return jsonify(quest)
    return jsonify({"error": "Quest not found"}), 404

# Endpoint do dodawania nowego questa (używa metody POST)
@app.route("/quests", methods=["POST"])
def add_quest():
    new_quest = request.get_json()  # Pobiera dane w formacie JSON
    new_quest["id"] = len(database) + 1  # Nadaje nowe ID
    database.append(new_quest)
    return jsonify(new_quest), 201  # Zwraca dodany element

# Endpoint do aktualizacji statusu questa (używa metody PUT)
@app.route("/quests/<int:quest_id>", methods=["PUT"])
def update_quest(quest_id):
    quest = next((q for q in database if q["id"] == quest_id), None)
    if quest:
        data = request.get_json()
        quest["status"] = data.get("status", quest["status"])  # Aktualizuje status
        return jsonify(quest)
    return jsonify({"error": "Quest not found"}), 404

# Endpoint do usunięcia questa (używa metody DELETE)
@app.route("/quests/<int:quest_id>", methods=["DELETE"])
def delete_quest(quest_id):
    global database
    database = [q for q in database if q["id"] != quest_id]
    return jsonify({"message": "Quest deleted"}), 200

if __name__ == "__main__":
    app.run(port=3000)
