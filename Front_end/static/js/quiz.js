// Base URL for the trivia API
const API_BASE_URL = "http://localhost:5000/api";

let currentQuestionIndex = 0;
let numQuestions = 5;
let questions = [];
let score = 0;
let quizStarted = false;
let selectedDifficulty = "";

// Function to handle difficulty selection
function setSelectedDifficulty(difficulty) {
    selectedDifficulty = difficulty;
    console.log(`Selected Difficulty: ${selectedDifficulty}`);

    // Update the displayed difficulty on the page
    const formattedDifficulty = selectedDifficulty.charAt(0).toUpperCase() + selectedDifficulty.slice(1);
    document.getElementById("difficulty-display").innerText = formattedDifficulty;
}

// Function to start the quiz
async function startQuiz() {
    if (quizStarted) return; // Prevents duplicate execution
    if (!selectedDifficulty) {
        alert("Please select a difficulty level first!");
        return;
    }

    quizStarted = true;
    numQuestions = document.getElementById("numQuestions").value || 5;
    console.trace("startQuiz called");

    try {
        const response = await fetch(
            `${API_BASE_URL}/questions?difficulty=${selectedDifficulty}&num=${numQuestions}`
        );
        if (!response.ok) {
            throw new Error("Failed to fetch questions");
        }

        questions = await response.json();
        console.log("Fetched Questions:", questions);

        if (questions.length > 0) {
            currentQuestionIndex = 0;
            score = 0;
            displayQuestions(); // Modified to show all questions at once
            document.getElementById("quiz-content").style.display = "block";
            document.getElementById("scorecard").style.display = "none";
        } else {
            alert("No questions available for the selected difficulty.");
        }
    } catch (error) {
        console.error("Error:", error.message);
        alert("Failed to fetch questions. Please try again later.");
    }
}

// Function to display all questions at once
function displayQuestions() {
    const container = document.getElementById("questions-container");
    container.innerHTML = ''; // Clear the container before rendering new questions

    questions.forEach((question, index) => {
        const questionDiv = document.createElement("div");
        questionDiv.className = "question-container mb-4";
        questionDiv.innerHTML = `
            <h4 style="font-weight: bold; font-size: 1.5rem;">Question ${index + 1}: ${question.question}</h4>
            <div class="options">
                ${question.options.map(option => {
                    return `<button class="btn btn-outline-primary m-2" onclick="checkAnswer('${option}', ${index})">${option}</button>`;
                }).join('')}
            </div>
        `;
        container.appendChild(questionDiv);
    });
}

// Function to check the answer and update the score
function checkAnswer(selectedOption, questionIndex) {
    const correctAnswer = questions[questionIndex].answer;
    const options = document.querySelectorAll(`#questions-container .question-container:nth-child(${questionIndex + 1}) .options button`);
    
    // Remove any existing classes from all options
    options.forEach(optionButton => {
        optionButton.classList.remove("selected", "correct", "incorrect");
    });

    // Add the 'selected' class to the selected button
    const selectedButton = Array.from(options).find(button => button.innerText === selectedOption);
    selectedButton.classList.add("selected");

    // Add 'correct' or 'incorrect' class to the buttons based on the answer
    if (selectedOption === correctAnswer) {
        selectedButton.classList.add("correct");
    } else {
        selectedButton.classList.add("incorrect");

        // Highlight the correct answer if it was not selected
        const correctButton = Array.from(options).find(button => button.innerText === correctAnswer);
        correctButton.classList.add("correct");
    }

    // Log answer and update score
    if (selectedOption === correctAnswer) {
        score++;
    }

    console.log(
        `Question: ${questions[questionIndex].question}, Selected: ${selectedOption}, Correct: ${correctAnswer}, Score: ${score}`
    );

    // Move to the next question or show the scorecard
    if (questionIndex === questions.length - 1) {
        showScorecard();
    }
}

// Function to display the scorecard
function showScorecard() {
    document.getElementById("quiz-content").style.display = "none";
    document.getElementById("score").innerText = `${score} / ${questions.length}`;
    const percentage = (score / questions.length) * 100;
    document.getElementById("results").innerText = `${percentage.toFixed(2)}%`;
    document.getElementById("scorecard").style.display = "block";
}

// Function to restart the quiz
function restartQuiz() {
    // Reset quiz content and state
    document.getElementById('quiz-content').style.display = 'none';
    document.getElementById('scorecard').style.display = 'none';
    document.getElementById('start-btn').style.display = 'block';

    // Reset global state variables
    currentQuestionIndex = 0;
    score = 0;
    quizStarted = false;
    questions = [];

    // Clear questions display
    document.getElementById('questions-container').innerHTML = "";

    // Reinitialize event listeners for difficulty buttons
    attachDifficultyEventListeners();
    // Reset selected difficulty display
    document.getElementById("difficulty-display").innerText = "None";
}

// Function to attach event listeners for difficulty buttons
function attachDifficultyEventListeners() {
    const easyButton = document.getElementById('easy-button');
    const mediumButton = document.getElementById('medium-button');
    const hardButton = document.getElementById('hard-button');
    
    if (easyButton) {
        easyButton.addEventListener('click', function() {
            setSelectedDifficulty('easy');
        });
    }
    if (mediumButton) {
        mediumButton.addEventListener('click', function() {
            setSelectedDifficulty('medium');
        });
    }
    if (hardButton) {
        hardButton.addEventListener('click', function() {
            setSelectedDifficulty('hard');
        });
    }
}

// Event listener for the "Start Quiz" button
document.getElementById("start-btn").addEventListener("click", startQuiz);

// Initial setup
console.log("Quiz Script Loaded");

// Wait for the DOM to load before attaching event listeners for difficulty selection
document.addEventListener('DOMContentLoaded', function () {
    attachDifficultyEventListeners(); // Attach event listeners for difficulty buttons

    const restartButton = document.getElementById('restart-btn');
    if (restartButton) {
        restartButton.addEventListener('click', restartQuiz);
    }
});
