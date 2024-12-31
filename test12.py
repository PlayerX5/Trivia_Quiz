from flask import Flask, jsonify, request, session
from random import choice, sample
from collections import OrderedDict
import json
from flask_session import Session  # Import Flask-Session
import psycopg2
from psycopg2 import sql
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for sessions

# Configure server-side session storage
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on the server's filesystem
CORS(app, supports_credentials=True)  # Enable CORS with credentials support
app.config['SESSION_PERMANENT'] = False  # Sessions are not permanent
Session(app)  # Initialize Flask-Session

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        dbname="Trivia", 
        user="postgres", 
        password="password", 
        host="localhost", 
        port="5432"
    )
    return conn

# Function to fetch questions from the database
def get_questions(difficulty):
    conn = get_db_connection()
    cur = conn.cursor()

    # Ensure difficulty is treated as a string
    difficulty_str = str(difficulty).lower()

    # Use the correct SQL query with a string comparison for difficulty
    cur.execute("SELECT * FROM questions WHERE difficulty = %s", (difficulty_str,))
    questions = cur.fetchall()  # Fetch all rows as a list of tuples

    # Convert fetched data into a dictionary format similar to the original trivia_questions
    formatted_questions = []
    for row in questions:
        # print(row[2], type(row[2]))
        formatted_questions.append({
            "id": row[0],  # Assuming the first column is the ID
            "question": row[1],
            "options": row[2],  # Assuming options are comma-separated
            "answer": row[3],
            "difficulty": difficulty,
        })

    cur.close()
    conn.close()
    return formatted_questions

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
    
    # Fetch a random question from the database based on difficulty
    formatted_questions = get_questions(difficulty)
    if not formatted_questions:
        return jsonify({"error": f"No questions found for difficulty level: {difficulty}."}), 404

    # Pick a random question from the filtered list
    question = choice(formatted_questions)

    # Store the question's ID in the session for later validation
    session['last_question_ids'] = [question['id']]
    session['difficulty'] = difficulty  # Store the difficulty in the session
    app.logger.info(f"Selected question: {question}")  # Log only the selected question

    # Manually structure the response to ensure the correct order: id, question, options
    response = OrderedDict([
        ("id", question["id"]),
        ("question", question["question"]),
        ("options", question["options"]),
    ])
    
    # Return the formatted response with proper indentation
    return app.response_class(
        response=json.dumps(response, indent=4, ensure_ascii=False),
        mimetype='application/json'
    )

# Endpoint to retrieve multiple trivia questions based on difficulty
@app.route('/api/questions', methods=['GET'])
def get_multiple_questions():
    num_questions = request.args.get('num', default=1, type=int)  # Default to 1 question
    difficulty = request.args.get('difficulty', default='easy', type=str).lower()  # Normalize to lowercase

    app.logger.info(f"Received difficulty: {difficulty}, num_questions: {num_questions}")

    # Validate the difficulty input
    if difficulty not in ['easy', 'medium', 'hard']:
        return jsonify({"error": "Invalid difficulty level. Valid levels are 'easy', 'medium', and 'hard'."}), 400

    # Fetch questions based on difficulty
    formatted_questions = get_questions(difficulty)
    if not formatted_questions:
        return jsonify({"error": f"No questions found for difficulty level: {difficulty}."}), 404

    # Sample questions
    selected_questions = sample(formatted_questions, min(num_questions, len(formatted_questions)))

    # Store question IDs in the session
    session['last_question_ids'] = [q['id'] for q in selected_questions]
    session['difficulty'] = difficulty
    app.logger.info(f"Selected question: {selected_questions}")  # Log only the selected question

    # Format the response
    response = [
        OrderedDict([
            ("id", q["id"]),
            ("question", q["question"]),
            ("options", q["options"]),
        ]) for q in selected_questions
    ]

    return app.response_class(
        response=json.dumps(response, indent=4, ensure_ascii=False),
        mimetype='application/json'
    )

# Endpoint to check answers and calculate score
@app.route('/api/answer', methods=['POST'])
def check_answers():
    data = request.get_json()
    results = []
    correct_count = 0
    total_questions = 0

    # Debug: Log the received data and session state
    app.logger.info("Received data: %s", data)
    app.logger.info("Session state: %s", dict(session))

    # Retrieve the last served question(s) IDs from the session
    last_question_ids = session.get('last_question_ids', [])
    difficulty = session.get('difficulty', 'easy')  # Default to 'easy'

    if not last_question_ids:
        return jsonify({"error": "No question(s) have been served yet."}), 400

    # Fetch the previously served questions based on difficulty
    questions = get_questions(difficulty)

    for answer_data in data.get('answers', []):
        question_id = answer_data.get('id')
        selected_option = answer_data.get('answer')
        total_questions += 1

        # Validate the question ID
        if question_id not in last_question_ids:
            results.append({"id": question_id, "error": "Question ID does not match any of the previously served question IDs"})
            continue

        # Find the question by ID
        trivia = next((q for q in questions if q['id'] == question_id), None)
        if not trivia:
            results.append({"id": question_id, "error": "Invalid question ID"})
            continue

        # Ensure options are in list form
        trivia['options'] = trivia['options'].split(',') if isinstance(trivia['options'], str) else trivia['options']

        # Validate the selected option
        if selected_option not in trivia['options']:
            results.append({"id": question_id, "error": "Invalid option"})
            continue

        # Check if the selected answer is correct
        if trivia['answer'].strip().lower() == selected_option.strip().lower():
            correct_count += 1
            results.append({"id": question_id, "correct": True, "message": "Correct answer!"})
        else:
            results.append({"id": question_id, "correct": False, "message": "Wrong answer. Try again!"})

    # Calculate the score
    score = {
        "total_attempted": total_questions,
        "correct_answers": correct_count,
        "score_percentage": (correct_count / total_questions) * 100 if total_questions > 0 else 0
    }

    return jsonify({
        "results": results,
        "score": score
    })

if __name__ == '__main__':
    app.run(debug=True)


# Connected with the database.