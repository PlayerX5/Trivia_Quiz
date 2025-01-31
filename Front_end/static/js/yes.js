const yesBtn = document.querySelector("#option-yes"); // "Yes" button

// Redirect to a new page on click
yesBtn.addEventListener("click", () => {
  if (difficultySelector.value !== "") { // Ensure difficulty is selected
    window.location.href = `quiz.html?difficulty=${difficultySelector.value}`;
  } else {
    alert("Please select a difficulty level before starting the quiz.");
  }
});
