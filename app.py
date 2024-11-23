from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session tracking

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Initialize user performance in session
@app.before_request
def initialize_session():
    if "quiz_state" not in session:
        session["quiz_state"] = {"question_count": 0, "correct": 0, "incorrect": 0}

# Function to update quiz state
def update_quiz_state(correct):
    if correct:
        session["quiz_state"]["correct"] += 1
    else:
        session["quiz_state"]["incorrect"] += 1
    session["quiz_state"]["question_count"] += 1


# Function to update performance
def update_performance(correct):
    if correct:
        session["performance"]["correct"] += 1
    else:
        session["performance"]["incorrect"] += 1

# Route to reset performance (optional)
@app.route('/reset-performance')
def reset_performance():
    session["performance"] = {"correct": 0, "incorrect": 0}
    return jsonify({"message": "Performance reset"})

# Route for the Learn page
@app.route('/learn')
def learn():
    return render_template('learn.html')

# Route for the Practice page
@app.route('/practice')
def practice():
    return render_template('practice.html')

# Route for the Quiz page
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

# @app.route('/api/question', methods=['GET'])
# def get_question():
#     question, correct_answer, explanation = generate_subjunctive_question()
#     return jsonify({'question': question, 'answer': correct_answer, 'explanation': explanation})

# subjunctive_triggers = [
#     ("demander que", "to ask that"), 
#     ("vouloir que", "to want that"), 
#     ("il est important que", "it is important that"),
#     ("il est nécessaire que", "it is necessary that"), 
#     ("il faut que", "it is necessary that"), 
#     ("il vaut mieux que", "it is better that"),
#     ("avoir peur que", "to be afraid that"), 
#     ("craindre que", "to fear that"),
#     # Add more triggers as needed with explanations
# ]

irregular_verbs_subjunctive = {
    "avoir": ["aie", "aies", "ait", "ayons", "ayez", "aient"],
    "être": ["sois", "sois", "soit", "soyons", "soyez", "soient"],
    "faire": ["fasse", "fasses", "fasse", "fassions", "fassiez", "fassent"],
    "aller": ["aille", "ailles", "aille", "allions", "alliez", "aillent"]
    # Add more irregular verbs if needed
}

# @app.route('/api/question', methods=['GET'])
# def get_question():
#     question, correct_answer, explanation = generate_subjunctive_question()
#     print(f"Generated Question: {question}, Answer: {correct_answer}, Explanation: {explanation}")  # Debug
#     return jsonify({'question': question, 'answer': correct_answer, 'explanation': explanation})

@app.route('/api/question', methods=['GET'])
def get_question():
    # Ensure we initialize session variables for quiz
    if "questions_asked" not in session:
        session["questions_asked"] = 0
        session["performance"] = {"correct": 0, "incorrect": 0}

    # End the quiz if 10 questions have been asked
    if session["questions_asked"] >= 10:
        return jsonify({
            "quiz_end": True,
            "score": session["performance"]["correct"],
            "total_questions": session["questions_asked"]
        })

    # Increment questions asked
    session["questions_asked"] += 1

    # Generate the question
    question, correct_answer, explanation = generate_subjunctive_question()

    # Debug output
    print(f"Generated Question: {question}, Correct Answer: {correct_answer}")

    return jsonify({
        "quiz_end": False,
        "question": question,
        "correct_answer": correct_answer,
        "score": session["performance"]["correct"]  # Include current score
    })


@app.route('/api/answer', methods=['POST'])
def submit_answer():
    # Parse user answer from the request
    user_answer = request.json.get("answer", "").strip()
    correct_answer = request.json.get("correct_answer", "").strip()

    # Check if the answer is correct
    is_correct = user_answer == correct_answer

    # Update performance
    if is_correct:
        session["performance"]["correct"] += 1
    else:
        session["performance"]["incorrect"] += 1

    # Respond with feedback
    return jsonify({
        "correct": is_correct,
        "message": "Correct!" if is_correct else f"Incorrect. The correct answer was: {correct_answer}",
        "score": session["performance"]["correct"]
    })

subjunctive_triggers = [
    ("demander que", "to ask that"), 
    ("vouloir que", "to want that"), 
    ("il est important que", "it is important that"),
    ("il est nécessaire que", "it is necessary that"), 
    ("il faut que", "it is necessary that"), 
    ("il vaut mieux que", "it is better that"),
    ("avoir peur que", "to be afraid that"), 
    ("craindre que", "to fear that"),
    # Add more triggers as needed
]

# def generate_subjunctive_question():
#     # Select a random subjunctive trigger and explanation
#     trigger, trigger_explanation = random.choice(subjunctive_triggers)

#     # Select a random verb and its conjugations
#     verb, conjugations = random.choice(list(irregular_verbs_subjunctive.items()))

#     # Select a random subject pronoun and its conjugation
#     subject_pronouns = ["je", "tu", "il/elle/on", "nous", "vous", "ils/elles"]
#     subject = random.choice(subject_pronouns)
#     pronoun_index = subject_pronouns.index(subject)
#     correct_conjugation = conjugations[pronoun_index]

#     # Construct the question text and explanation
#     question_text = f"{trigger} {subject} ({verb}) ______"
#     explanation = f"'{trigger}' triggers the subjunctive because it expresses {trigger_explanation}."
#     return question_text, correct_conjugation, explanation

def generate_subjunctive_question():
    # Define difficulty levels
    easy_triggers = subjunctive_triggers[:3]  # First few triggers for simplicity
    medium_triggers = subjunctive_triggers[3:6]
    hard_triggers = subjunctive_triggers[6:]

    easy_verbs = {"être": ["suis", "es", "est", "sommes", "êtes", "sont"]}
    medium_verbs = irregular_verbs_subjunctive
    hard_verbs = irregular_verbs_subjunctive

    # Determine difficulty based on performance
    correct = session["performance"]["correct"]
    incorrect = session["performance"]["incorrect"]

    if correct < 3:
        difficulty = "easy"
        triggers = easy_triggers
        verbs = easy_verbs
    elif correct < 6:
        difficulty = "medium"
        triggers = medium_triggers
        verbs = medium_verbs
    else:
        difficulty = "hard"
        triggers = hard_triggers
        verbs = hard_verbs

    # Select a random trigger and verb based on difficulty
    trigger, trigger_explanation = random.choice(triggers)
    verb, conjugations = random.choice(list(verbs.items()))

    # Select a random subject pronoun and its conjugation
    subject_pronouns = ["je", "tu", "il/elle/on", "nous", "vous", "ils/elles"]
    subject = random.choice(subject_pronouns)
    pronoun_index = subject_pronouns.index(subject)
    correct_conjugation = conjugations[pronoun_index]

    # Construct the question text
    question_text = f"{trigger} {subject} ({verb}) ______"
    explanation = f"'{trigger}' triggers the subjunctive because it expresses {trigger_explanation}. This is a {difficulty} question."
    return question_text, correct_conjugation, explanation

if __name__ == '__main__':
    app.run(debug=True)
