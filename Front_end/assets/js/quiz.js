let questions = [];
let selectedDifficulty = "";
let answers = []; // To store selected answers for submission

// Show number of questions input after difficulty is selected
function selectDifficulty(difficulty) {
    selectedDifficulty = difficulty;
    document.getElementById('difficulty-selector').style.display = 'none';
    document.getElementById('num-questions-container').style.display = 'block';
    console.log(`Selected Difficulty: ${selectedDifficulty}`); // Debugging the selected value
}

// Start the quiz
function startQuiz() {
    const numQuestions = document.getElementById('numQuestions').value;

    if (!selectedDifficulty) { // Check if difficulty is selected
        alert("Please select a difficulty level before starting the quiz.");
        return;
    }
    
    const normalizedDifficulty = selectedDifficulty.toLowerCase(); // Normalize to lowercase
    const apiUrl = `http://127.0.0.1:5000/api/questions?difficulty=${normalizedDifficulty}&num=${numQuestions}`;

    console.log(`API URL: ${apiUrl}`); // Debugging the API URL

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error); // Show error from API
                return;
            }
            questions = data;
            displayAllQuestions();
            document.getElementById('quiz-content').style.display = 'block';
            document.getElementById('num-questions-container').style.display = 'none';
        })
        .catch(error => {
            console.error('Error fetching questions:', error);
            alert('Failed to load questions. Please try again later.');
        });
}

// Display all questions at once
function displayAllQuestions() {
    const questionsContainer = document.getElementById('questions-container');
    questionsContainer.innerHTML = ''; // Clear previous content

    questions.forEach((question, questionIndex) => {
        const questionEl = document.createElement('div');
        questionEl.className = 'question-block';
        questionEl.innerHTML = `
            <div class="question">${questionIndex + 1}. ${question.question}</div>
            <div class="options">
                ${question.options
                    .map(
                        (option, index) => `
                    <label>
                        <input type="radio" name="question-${question.id}" value="${option}">
                        ${option}
                    </label>
                `
                    )
                    .join('')}
            </div>
        `;
        questionsContainer.appendChild(questionEl);
    });

    document.getElementById('submit-btn').style.display = 'block';
}

// Submit answers to the backend
function submitAnswers() {
    answers = [];
    questions.forEach((question) => {
        const selectedOption = document.querySelector(`input[name="question-${question.id}"]:checked`);
        if (selectedOption) {
            answers.push({
                id: question.id,
                answer: selectedOption.value,
            });
        }
    });

    if (answers.length < questions.length) {
        alert('Please answer all questions.');
        return;
    }

    fetch('http://127.0.0.1:5000/api/answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ answers }),
    })
        .then(response => response.json())
        .then(data => {
            alert('Quiz submitted successfully!');
            displayScorecard(); // Show the scorecard or success message
        })
        .catch(error => {
            console.error('Error submitting answers:', error);
            alert('Failed to submit answers. Please try again.');
        });
}

// Display scorecard (optional based on backend response)
function displayScorecard() {
    document.getElementById('quiz-content').style.display = 'none';
    document.getElementById('scorecard').style.display = 'block';
    document.getElementById('score').innerText = `${answers.length} / ${questions.length}`;
}

// Restart the quiz
function restartQuiz() {
    document.getElementById('difficulty-selector').style.display = 'block';
    document.getElementById('quiz-content').style.display = 'none';
    document.getElementById('scorecard').style.display = 'none';
    questions = [];
    answers = [];
}
