from flask import Flask, jsonify, request, session
from random import choice, sample
from collections import OrderedDict
import json
from flask_session import Session  # Import Flask-Session
import psycopg2
from psycopg2 import sql

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for sessions

# Configure server-side session storage
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on the server's filesystem
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
def get_questions_from_db(difficulty=None, limit=1):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to get questions based on difficulty
    query = sql.SQL("SELECT id, question, options, answer, difficulty FROM questions")
    
    if difficulty:
        query += sql.SQL(" WHERE difficulty = %s")
    
    query += sql.SQL(" ORDER BY RANDOM() LIMIT %s")
    
    cursor.execute(query, (difficulty, limit) if difficulty else (limit,))
    rows = cursor.fetchall()

    # Convert rows into a list of dictionaries
    questions = []
    for row in rows:
        question = {
            'id': row[0],
            'question': row[1],
            'options': row[2],  # Assuming options are stored as a JSON array in the DB
            'answer': row[3],
            'difficulty': row[4]
        }
        questions.append(question)
        
    cursor.close()
    conn.close()
    print(row[2], type(row[2]))
    return questions

@app.before_request
def debug_session():
    print("Session data before request:", dict(session))  # Log session data before handling the request

# Endpoint to retrieve a random trivia question
@app.route('/api/trivia', methods=['GET'])
def get_trivia():
    difficulty = request.args.get('difficulty', default='easy', type=str).lower().capitalize()  # Default to 'easy'

    # Validate the difficulty input
    if difficulty not in ['Easy', 'Medium', 'Hard']:
        return jsonify({"error": "Invalid difficulty level. Valid levels are 'Easy', 'Medium', and 'Hard'."}), 400

    # Fetch a random question from the database based on difficulty
    questions = get_questions_from_db(difficulty=difficulty)

    if not questions:
        return jsonify({"error": f"No questions found for difficulty level: {difficulty}."}), 404

    # Pick a random question from the filtered list
    question = choice(questions)

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
# Endpoint to retrieve a set of trivia questions
@app.route('/api/questions', methods=['GET'])
def get_multiple_questions():
    num_questions = request.args.get('num', default=1, type=int)  # Default to 1 question
    difficulty = request.args.get('difficulty', default='Easy', type=str).lower().capitalize()  # Default to 'easy'
    
    # Validate the difficulty input
    if difficulty not in ['Easy', 'Medium', 'Hard']:
        return jsonify({"error": "Invalid difficulty level. Valid levels are 'Easy', 'Medium', and 'Hard'."}), 400

    # Fetch the requested number of questions from the database based on difficulty
    questions = get_questions_from_db(difficulty=difficulty, limit=num_questions)

    if not questions:
        return jsonify({"error": f"No questions found for difficulty level: {difficulty}."}), 404
    
    # Randomly sample the questions
    selected_questions = sample(questions, min(num_questions, len(questions)))

    # Store the IDs of the selected questions in the session for later validation
    session['last_question_ids'] = [q['id'] for q in questions]

    response = [
        OrderedDict([
            ("id", q["id"]),
            ("question", q["question"]),
            ("options", q["options"]),
        ]) for q in questions
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

    print("Received data:", data)  # Log the received data
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

        # Fetch the question from the database
        trivia = get_questions_from_db(difficulty=None, limit=1)
        trivia = next((q for q in trivia if q['id'] == question_id), None)
        if not trivia:
            # Add error if the question ID is invalid
            results.append({"id": question_id, "error": "Invalid question ID"})
            continue

        # Check if the selected option is valid and correct
        if selected_option not in trivia['options']:
            results.append({"id": question_id, "error": "Invalid option"})
            continue
        # Check if the selected option is correct
        elif trivia['answer'].lower() == selected_option.lower():
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
