document.addEventListener('DOMContentLoaded', () => {
    const commandInput = document.getElementById('command-input');
    const practiceSession = document.getElementById('practice-session');
    let questionCount = 1; // Track question numbers
    let currentAnswer = ''; // Stores the correct answer for evaluation

    // Function to fetch a new question from the server
    async function fetchQuestion() {
        try {
            const response = await fetch('/api/question');
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            displayQuestion(data.question);
            currentAnswer = data.answer;
        } catch (error) {
            console.error("Error fetching question:", error);
            displayFeedback("Error fetching question. Please try again.");
        }
    }

    // Display a new question in the practice session
    function displayQuestion(questionText) {
        // Create a container for each question, answer input, and feedback
        const questionContainer = document.createElement('div');
        questionContainer.className = 'question-container';

        // Display question text
        const questionElement = document.createElement('p');
        questionElement.textContent = `Question ${questionCount}: ${questionText}`;
        questionContainer.appendChild(questionElement);

        // Display input for the answer
        const answerInput = document.createElement('input');
        answerInput.type = 'text';
        answerInput.placeholder = "Ta réponse ?";
        answerInput.className = 'answer-input';
        questionContainer.appendChild(answerInput);

        // Display feedback element (initially empty)
        const feedbackElement = document.createElement('p');
        feedbackElement.className = 'feedback';
        questionContainer.appendChild(feedbackElement);

        // Append question container to the practice session
        practiceSession.appendChild(questionContainer);

        // Focus on the answer input for immediate response
        answerInput.focus();

        // Listen for Enter key to submit the answer or "quitter" command
        answerInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                const userAnswer = answerInput.value.trim().toLowerCase();
                if (userAnswer === 'quitter') {
                    endPracticeSession();
                } else {
                    checkAnswer(userAnswer, feedbackElement);
                }
            }
        });

        questionCount++; // Increment question count for next question
    }

    // Check if the user's answer is correct
    function checkAnswer(userAnswer, feedbackElement) {
        if (userAnswer.toLowerCase() === currentAnswer.toLowerCase()) {
            feedbackElement.textContent = `Bravo ! C'est la bonne réponse : '${currentAnswer}'.`;
        } else {
            feedbackElement.textContent = `Pas tout à fait ! La bonne réponse est '${currentAnswer}'.`;
        }
        // Fetch a new question after providing feedback
        fetchQuestion();
    }

    // End the practice session
    function endPracticeSession() {
        practiceSession.innerHTML = ''; // Clear all questions and feedback
        displayFeedback("La pratique est terminée. Au revoir!");
    }

    // Display feedback message (e.g., errors or session end)
    function displayFeedback(message) {
        const feedback = document.createElement('p');
        feedback.className = 'feedback';
        feedback.textContent = message;
        practiceSession.appendChild(feedback);
    }

    // Listen for 'commencer' or 'quitter' commands in the command input
    commandInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            const command = commandInput.value.trim().toLowerCase();
            if (command === 'commencer') {
                practiceSession.innerHTML = ''; // Clear previous session content
                fetchQuestion(); // Start generating questions
                commandInput.value = ''; // Clear the command input
            } else if (command === 'quitter') {
                endPracticeSession();
                commandInput.value = ''; // Clear the command input
            }
        }
    });
});
