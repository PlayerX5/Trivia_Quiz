from flask import Flask, jsonify, request, session
from random import choice, sample
from collections import OrderedDict
import json
from flask_session import Session  # Import Flask-Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for sessions

# Configure server-side session storage
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on the server's filesystem
app.config['SESSION_PERMANENT'] = False  # Sessions are not permanent
Session(app)  # Initialize Flask-Session

# Sample trivia questions database with options and difficulty levels
trivia_questions = [
    {
        "id": 1,
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "answer": "Paris",
        "difficulty": "easy"
    },
    {
        "id": 2,
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["Mark Twain", "Charles Dickens", "William Shakespeare", "Jane Austen"],
        "answer": "William Shakespeare",
        "difficulty": "medium"
    },
    {
        "id": 3,
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "answer": "4",
        "difficulty": "easy"
    },
    {
        "id": 4,
        "question": "What is the capital of India?",
        "options": ["Rajasthan", "Delhi", "Karnataka", "Nepal"],
        "answer": "Delhi",
        "difficulty": "medium"
    },
    {
        "id": 5,
        "question": "What is 5*5?",
        "options": ["15", "20", "25", "30"],
        "answer": "25",
        "difficulty": "hard"
    },
    {
        "id": 6,
        "question": "What is the square root of 144?",
        "options": ["10", "12", "14", "16"],
        "answer": "12",
        "difficulty": "hard"
    },
    {
        "id": 7,
        "question": "Who developed the theory of relativity?",
        "options": ["Newton", "Einstein", "Galileo", "Tesla"],
        "answer": "Einstein",
        "difficulty": "hard"
    }
]

@app.before_request
def debug_session():
    print("Session data before request:", dict(session))  # Log session data before handling the request

# Endpoint to retrieve a random trivia question
@app.route('/api/trivia', methods=['GET'])
def get_trivia():
    difficulty = request.args.get('difficulty', default='easy', type=str).lower()  # Default to 'easy'

    # Validate the difficulty input
    if difficulty not in ['easy', 'medium', 'hard']:
        return jsonify({"error": "Invalid difficulty level. Valid levels are 'easy', 'medium', and 'hard'."}), 400

    # Filter questions by difficulty
    filtered_questions = [q for q in trivia_questions if q['difficulty'] == difficulty]

    if not filtered_questions:
        return jsonify({"error": f"No questions found for difficulty level: {difficulty}."}), 404

    # Pick a random question from the filtered list
    question = choice(filtered_questions)

    # Store the question's ID in the session for later validation
    session['last_question_id'] = question['id']

    response = OrderedDict([
        ("id", question["id"]),
        ("question", question["question"]),
        ("options", question["options"]),
    ])

    return app.response_class(
        response=json.dumps(response, indent=4),
        mimetype='application/json'
    )

# Endpoint to retrieve multiple trivia questions based on difficulty
@app.route('/api/questions', methods=['GET'])
def get_multiple_questions():
    num_questions = request.args.get('num', default=1, type=int)  # Default to 1 question
    difficulty = request.args.get('difficulty', default='easy', type=str).lower()  # Default to 'easy'

    # Ensure num_questions doesn't exceed the total number of available questions
    if num_questions > len(trivia_questions):
        return jsonify({"error": f"Only {len(trivia_questions)} questions are available."}), 400
    
    # Validate the difficulty input
    if difficulty not in ['easy', 'medium', 'hard']:
        return jsonify({"error": "Invalid difficulty level. Valid levels are 'easy', 'medium', and 'hard'."}), 400

    # Filter questions by difficulty
    filtered_questions = [q for q in trivia_questions if q['difficulty'] == difficulty]

    if not filtered_questions:
        return jsonify({"error": f"No questions found for difficulty level: {difficulty}."}), 404
    
    # Randomly sample the questions
    selected_questions = sample(filtered_questions, min(num_questions, len(filtered_questions)))

    # Store the IDs of the selected questions in the session for later validation
    session['last_question_ids'] = [q['id'] for q in selected_questions] # Store IDs in the session

    # Manually structure the response to ensure the correct order: id, question, options
    response = [
        OrderedDict([
            ("id", q["id"]),
            ("question", q["question"]),
            ("options", q["options"]),
        ]) for q in selected_questions
    ]
    # Return the formatted response with proper indentation
    return app.response_class(
        response=json.dumps(response, indent=4),  # Add indent for pretty printing
        mimetype='application/json'
    )

# Endpoint to check answers and calculate score
@app.route('/api/answer', methods=['POST'])
def check_answers():
    data = request.get_json()
    results = []
    correct_count = 0  # Track correct answers
    total_questions = 0  # Track total attempted questions

    print("Received data:", data)
    print("Session data at start of /api/answer:", dict(session))

    # Retrieve the last served question(s) IDs from the session
    last_question_ids = session.get('last_question_ids')

    print("Session at the start of /api/answer:", session)  # Log session data
    print("Last Question IDs in session:", last_question_ids)  # Log session data

    # Ensure the question IDs are valid
    if not last_question_ids:
        return jsonify({"error": "No question(s) have been served yet."}), 400

    # Process each answer in the list
    for answer_data in data.get('answers', []):
        question_id = answer_data.get('id')  # Extract `id` from the answer payload
        selected_option = answer_data.get('answer')

        print(f"Processing answer for question ID {question_id} with selected option '{selected_option}'")
        total_questions += 1  # Increment total questions count

        # Check if the question ID matches the session data
        if question_id not in last_question_ids:
            results.append({"id": question_id, "error": "Question ID does not match any of the previously asked question IDs"})
            continue

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

        # Check if the selected option is correct
        if trivia['answer'].lower() == selected_option.lower():
            correct_count += 1  # Increment correct answers count
            results.append({"id": question_id, "correct": True, "message": "Correct answer!"})
        else:
            results.append({"id": question_id, "correct": False, "message": "Wrong answer. Try again!"})

    print("Results:", results)  # Log the results

    # Calculate the score
    score = {
        "total_attempted": total_questions,
        "correct_answers": correct_count,
        "score_percentage": (correct_count / total_questions) * 100 if total_questions > 0 else 0
    }

    return jsonify({
        "results": results,
        "score": score  # Include the score in the response
    })

if __name__ == '__main__':
    app.run(debug=True)

# Has the proper ordering of questions, matches the GET and POST questions, Able to choose the number of questions,
# Submit answer for specific answer, retrieve the score, and added difficulty.