from flask import Flask, jsonify, request
from random import choice, sample
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

# Endpoint to retrieve a set of trivia questions
@app.route('/api/questions', methods=['GET'])
def get_multiple_questions():
    # Get the number of questions requested by the user
    num_questions = request.args.get('num', default=1, type=int)
    
    # Ensure num_questions doesn't exceed the total number of available questions
    if num_questions > len(trivia_questions):
        return jsonify({"error": f"Only {len(trivia_questions)} questions are available."}), 400
    
    # Randomly sample the questions
    selected_questions = sample(trivia_questions, num_questions)

    # Return the selected questions
    return jsonify([{
        "id": q["id"],
        "question": q["question"],
        "options": q["options"]
    } for q in selected_questions])

# Endpoint to check the answer
@app.route('/api/answer', methods=['POST'])
def check_answers():
    data = request.get_json()
    results = []

    # Process each answer in the list
    for answer_data in data.get('answers', []):
        question_id = answer_data.get('id')
        selected_option = answer_data.get('answer')

        # Find the question by ID
        trivia = next((q for q in trivia_questions if q['id'] == question_id), None)
        if not trivia:
            # Add error if the question ID is invalid
            results.append({"id": question_id, "error": "Invalid question ID"})
            continue

        # Check if the selected option is in the list of valid options
        if selected_option not in trivia['options']:
            results.append({"id": question_id, "error": "Invalid option"})
            continue

        # Check if the selected option is the correct answer
        if trivia['answer'].lower() == selected_option.lower():
            results.append({"id": question_id, "correct": True, "message": "Correct answer!"})
        else:
            results.append({"id": question_id, "correct": False, "message": "Wrong answer. Try again!"})

    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)





#Added the option of choosing the number of questions