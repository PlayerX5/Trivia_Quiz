from flask import Flask, jsonify, request
from random import choice
from collections import OrderedDict

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
    }
]

# Endpoint to retrieve a random trivia question
@app.route('/api/trivia', methods=['GET'])
def get_trivia():
    question = choice(trivia_questions)  # Pick a random question
    response = OrderedDict([
        ("id", question["id"]),
        ("question", question["question"]),
        ("options", question["options"]),
    ])
    print(response)
    return jsonify(response)

# Endpoint to check the answer
@app.route('/api/answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    question_id = data.get('id')
    selected_option = data.get('answer')

    # Find the correct answer for the question ID
    trivia = next((q for q in trivia_questions if q['id'] == question_id), None)
    if trivia:
        if trivia['answer'].lower() == selected_option.lower():
            return jsonify({"correct": True, "message": "Correct answer!"})
        else:
            return jsonify({"correct": False, "message": "Wrong answer. Try again!"})
    else:
        return jsonify({"error": "Invalid question ID"}), 400

if __name__ == '__main__':
    app.run(debug=True)



# Just question and answer. Doesn't see whether GET and POST are matching or not