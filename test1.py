from flask import Flask, jsonify, request
from random import choice

app = Flask(__name__)

# Sample trivia questions database (could be a file or database in production)
trivia_questions = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "Who wrote 'Romeo and Juliet'?", "answer": "William Shakespeare"},
    {"question": "What is 2 + 2?", "answer": "4"}
]

# Endpoint to retrieve a random trivia question
@app.route('/api/trivia', methods=['GET'])
def get_trivia():
    question = choice(trivia_questions)  # Pick a random question
    return jsonify(question)

# Endpoint to check the answer
@app.route('/api/answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')
    
    # Find the correct answer in the trivia_questions list
    trivia = next((q for q in trivia_questions if q['question'] == question), None)
    if trivia and trivia['answer'].lower() == answer.lower():
        return jsonify({"correct": True, "message": "Correct answer!"})
    return jsonify({"correct": False, "message": "Wrong answer. Try again!"})

if __name__ == '__main__':
    app.run(debug=True)




# Just Question and answer