from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from difflib import get_close_matches

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def load_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches = get_close_matches(user_question.lower(), [q.lower() for q in questions], n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, base: dict) -> str | None:
    for item in base["questions"]:
        if item["question"].lower() == question.lower():
            return item["answer"]
    return None

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message", "").strip()
        if not user_input:
            return jsonify({"response": "Please enter a valid message."}), 400

        fitness_base = load_base("fitness_base.json")
        questions = [item["question"] for item in fitness_base["questions"]]

        best_match = find_best_match(user_input, questions)
        if best_match:
            response = get_answer_for_question(best_match, fitness_base)
        else:
            response = "I don't know the answer to that yet. Teach me in the terminal mode!"

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": "Something went wrong on the server."}), 500

if __name__ == "__main__":
    app.run(debug=True)
