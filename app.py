from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/api/question', methods=['GET'])
def get_question():
    question, correct_answer, explanation = generate_subjunctive_question()
    return jsonify({'question': question, 'answer': correct_answer, 'explanation': explanation})

subjunctive_triggers = [
    ("demander que", "to ask that"), 
    ("vouloir que", "to want that"), 
    ("il est important que", "it is important that"),
    ("il est nécessaire que", "it is necessary that"), 
    ("il faut que", "it is necessary that"), 
    ("il vaut mieux que", "it is better that"),
    ("avoir peur que", "to be afraid that"), 
    ("craindre que", "to fear that"),
    # Add more triggers as needed with explanations
]

irregular_verbs_subjunctive = {
    "avoir": ["aie", "aies", "ait", "ayons", "ayez", "aient"],
    "être": ["sois", "sois", "soit", "soyons", "soyez", "soient"],
    "faire": ["fasse", "fasses", "fasse", "fassions", "fassiez", "fassent"],
    "aller": ["aille", "ailles", "aille", "allions", "alliez", "aillent"]
    # Add more irregular verbs if needed
}

def generate_subjunctive_question():
    # Select a random subjunctive trigger and explanation
    trigger, trigger_explanation = random.choice(subjunctive_triggers)

    # Select a random verb and its conjugations
    verb, conjugations = random.choice(list(irregular_verbs_subjunctive.items()))

    # Select a random subject pronoun and its conjugation
    subject_pronouns = ["je", "tu", "il/elle/on", "nous", "vous", "ils/elles"]
    subject = random.choice(subject_pronouns)
    pronoun_index = subject_pronouns.index(subject)
    correct_conjugation = conjugations[pronoun_index]

    # Construct the question text and explanation
    question_text = f"{trigger} {subject} ({verb}) ______"
    explanation = f"'{trigger}' triggers the subjunctive because it expresses {trigger_explanation}."
    return question_text, correct_conjugation, explanation

if __name__ == '__main__':
    app.run(debug=True)
