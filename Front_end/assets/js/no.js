document.addEventListener("DOMContentLoaded", () => {
  const difficultySelector = document.querySelector("#difficulty-selector"); // Dropdown selector
  const noBtn = document.querySelector("#option-no"); // "No" button

  // Add hover functionality to move the "No" button randomly
  noBtn.addEventListener("mouseover", () => {
    // Check if the selected difficulty is "Easy"
    if (difficultySelector.value === "easy") {
      const optionsContainer = document.querySelector("#options-container"); // Parent container
      const containerRect = optionsContainer.getBoundingClientRect(); // Get container's bounds
      const noBtnRect = noBtn.getBoundingClientRect(); // Get button's current bounds

      // Calculate max X and Y to ensure the button stays inside the parent container
      const maxX = containerRect.width - noBtnRect.width;
      const maxY = containerRect.height - noBtnRect.height;

      // Generate random positions within the parent container
      const randomX = Math.floor(Math.random() * maxX);
      const randomY = Math.floor(Math.random() * maxY);

      // Set new positions
      noBtn.style.position = "absolute"; // Ensure the button is positioned absolutely
      noBtn.style.left = randomX + "px";
      noBtn.style.top = randomY + "px";
    }
  });
});