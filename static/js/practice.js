document.addEventListener('DOMContentLoaded', () => {
    const commandInput = document.getElementById('command-input');
    const practiceQuestion = document.getElementById('practice-question');
    const answerInput = document.getElementById('answer-input');
    const submitAnswerButton = document.getElementById('submit-answer');
    const feedback = document.getElementById('feedback');
    let currentAnswer = ''; // Stores the correct answer for the current question

    // Function to load a new question
    async function loadPracticeQuestion() {
        try {
            const response = await fetch('/api/question');
            const data = await response.json();
            practiceQuestion.textContent = data.question;
            currentAnswer = data.answer;
            answerInput.style.display = 'block';
            submitAnswerButton.style.display = 'block';
            // feedback.textContent = ''; // Clear previous feedback
        } catch (error) {
            console.error("Error loading question:", error);
            feedback.textContent = "Error loading question. Please try again.";
        }
    }

    // Event listener for command input
    commandInput.addEventListener('keyup', (event) => {
        if (event.key === 'Enter') {
            const command = commandInput.value.trim().toLowerCase();
            if (command === 'commencer') {
                loadPracticeQuestion(); // Start the practice session
                feedback.textContent = "Practice session started!";
                commandInput.value = ''; // Clear input field
            } else if (command === 'quitter') {
                // Stop the practice session
                practiceQuestion.textContent = '';
                answerInput.style.display = 'none';
                submitAnswerButton.style.display = 'none';
                feedback.textContent = "Practice session stopped.";
                commandInput.value = ''; // Clear input field
            }
        }
    });

    // Event listener for submitting an answer
    submitAnswerButton.addEventListener('click', () => {
        const userAnswer = answerInput.value.trim().toLowerCase(); // Define userAnswer here
        console.log("User Answer:", userAnswer); // For debugging
        console.log("Correct Answer:", currentAnswer); // For debugging

        if (userAnswer === currentAnswer.toLowerCase()) {
            feedback.innerHTML = "<span style='color: green;'>Correct!</span>";
        } else {
            feedback.innerHTML = `<span style='color: red;'>Incorrect. The correct answer is '${currentAnswer}'.</span>`;
        }

        answerInput.value = ''; // Clear answer input field
        loadPracticeQuestion(); // Load a new question after submitting
    });
});
