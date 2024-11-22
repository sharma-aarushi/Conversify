document.addEventListener('DOMContentLoaded', () => {
    const quizQuestionText = document.getElementById('quiz-question-text');
    const quizAnswerInput = document.getElementById('quiz-answer-input');
    const submitQuizAnswerButton = document.getElementById('submit-quiz-answer');
    const quizFeedback = document.getElementById('quiz-feedback');
    const quizScoreText = document.getElementById('quiz-score');
    const restartQuizButton = document.getElementById('restart-quiz');

    let currentAnswer = ''; // Stores the correct answer for the current question
    let explanationText = ''; // Stores explanation for the current question
    let score = 0; // Initialize score
    let questionCount = 0; // Track number of questions asked

    const MAX_QUESTIONS = 10; // Set the number of questions per session

    // Function to load a new quiz question
    async function loadQuizQuestion() {
        if (questionCount >= MAX_QUESTIONS) {
            endQuiz(); // End quiz if question limit is reached
            return;
        }

        try {
            const response = await fetch('/api/question');
            const data = await response.json();

            quizQuestionText.textContent = data.question;
            currentAnswer = data.answer;
            explanationText = data.explanation;
            quizAnswerInput.value = '';
            quizFeedback.textContent = '';

            questionCount++;
            quizScoreText.textContent = `Score: ${score} | Question: ${questionCount}/${MAX_QUESTIONS}`;
        } catch (error) {
            quizFeedback.textContent = "Error loading question. Please try again.";
        }
    }

    // Call loadQuizQuestion initially to start the quiz
    loadQuizQuestion();

    // Submit quiz answer and provide feedback
    submitQuizAnswerButton.addEventListener('click', () => {
        const userAnswer = quizAnswerInput.value.trim().toLowerCase();

        // Clear any previous feedback styling
        quizFeedback.classList.remove('correct', 'incorrect');

        if (userAnswer === currentAnswer.toLowerCase()) {
            quizFeedback.innerHTML = `<span class="correct"><strong>Correct!</strong> ${explanationText}</span>`;
            score++;
        } else {
            quizFeedback.innerHTML = `<span class="incorrect"><strong>Incorrect!</strong> The correct answer is '${currentAnswer}'. ${explanationText}</span>`;
        }

        quizScoreText.textContent = `Score: ${score} | Question: ${questionCount}/${MAX_QUESTIONS}`;

        if (questionCount < MAX_QUESTIONS) {
            loadQuizQuestion();
        } else {
            endQuiz();
        }
    });

    // End the quiz
    function endQuiz() {
        quizQuestionText.textContent = '';
        quizAnswerInput.style.display = 'none';
        submitQuizAnswerButton.style.display = 'none';
        quizFeedback.innerHTML = `<strong>Quiz Completed!</strong> Your final score is ${score} out of ${MAX_QUESTIONS}.`;
    }

    // Restart the quiz
    restartQuizButton.addEventListener('click', () => {
        score = 0;
        questionCount = 0;
        quizAnswerInput.style.display = 'inline-block';
        submitQuizAnswerButton.style.display = 'inline-block';
        loadQuizQuestion();
    });
});
