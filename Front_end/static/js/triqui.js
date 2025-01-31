document.getElementById("difficulty-selector").addEventListener("change", function () {
    const difficulty = this.value;
    fetchQuestion(difficulty);
  });
  
  function fetchQuestion(difficulty) {
    fetch(`https://api.example.com/trivia?difficulty=${difficulty}`)
      .then((response) => response.json())
      .then((data) => {
        const questionData = data.results[0]; // Assuming the API returns an array of questions
        displayQuestion(questionData);
      })
      .catch((error) => {
        console.error("Error fetching question:", error);
      });
  }
  
  function displayQuestion(questionData) {
    const questionText = document.getElementById("question-text");
    const optionsContainer = document.getElementById("options-container");
  
    questionText.textContent = questionData.question;
    
    // Clear previous options
    optionsContainer.innerHTML = "";
  
    // Add new options
    questionData.incorrect_answers.forEach((answer, index) => {
      const option = document.createElement("button");
      option.textContent = answer;
      option.classList.add("option-button");
      option.addEventListener("click", () => checkAnswer(answer, questionData.correct_answer));
      optionsContainer.appendChild(option);
    });
  
    const correctOption = document.createElement("button");
    correctOption.textContent = questionData.correct_answer;
    correctOption.classList.add("option-button");
    correctOption.addEventListener("click", () => checkAnswer(questionData.correct_answer, questionData.correct_answer));
    optionsContainer.appendChild(correctOption);
  }
  
  function checkAnswer(selectedAnswer, correctAnswer) {
    if (selectedAnswer === correctAnswer) {
      alert("Correct!");
    } else {
      alert("Incorrect!");
    }
  }
  