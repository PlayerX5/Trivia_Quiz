from flask import Flask, jsonify, request
from random import choice
from collections import OrderedDict
import json

app = Flask(__name__)

# Sample trivia questions database with options and IDs
trivia_questions = [
    {
        "id": 1,
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "answer": "Paris"
    },
    {
        "id": 2,
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["Mark Twain", "Charles Dickens", "William Shakespeare", "Jane Austen"],
        "answer": "William Shakespeare"
    },
    {
        "id": 3,
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "answer": "4"
    },
    {
        "id": 4,
        "question": "What is the capital of India?",
        "options": ["Rajasthan", "Delhi", "Karnataka", "Nepal"],
        "answer": "Delhi"
    },
    {
        "id": 5,
        "question": "What is 5*5?",
        "options": ["15", "20", "25", "30"],
        "answer": "25"
    }
]

# Endpoint to retrieve a random trivia question
@app.route('/api/trivia', methods=['GET'])
def get_trivia():
    from collections import OrderedDict

    question = choice(trivia_questions)  # Pick a random question
    response = OrderedDict([
        ("id", question["id"]),
        ("question", question["question"]),
        ("options", question["options"]),
    ])
    return app.response_class(
        response=json.dumps(response, indent=4),  # Force JSON string
        mimetype='application/json'
    )

# Endpoint to check the answer
@app.route('/api/answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    question_id = data.get('id')
    selected_option = data.get('answer')

    # Find the question by ID
    trivia = next((q for q in trivia_questions if q['id'] == question_id), None)
    if not trivia:
        # Return error if the question ID is invalid
        return jsonify({"error": "Invalid question ID"}), 400

    # Check if the selected option is in the list of valid options
    if selected_option not in trivia['options']:
        return jsonify({"error": "Invalid option"}), 400

    # Check if the selected option is the correct answer
    if trivia['answer'].lower() == selected_option.lower():
        return jsonify({"correct": True, "message": "Correct answer!"})
    else:
        return jsonify({"correct": False, "message": "Wrong answer. Try again!"})

if __name__ == '__main__':
    app.run(debug=True)



# The order the ID, question and options was made proper