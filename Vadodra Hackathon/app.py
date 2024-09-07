from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session and flash to work

# User tracking
user_id = 101
course_id = 1
session_id = 1
user_understanding_level = 0.5  # Initial understanding level
question_difficulty = [0.5, 0.4, 0.8]  # Difficulty of each question

# Define the quiz questions and answers (this must be a list of dictionaries)
# Dekh Bhai Adarsh yaha quiz ke jaga tume database use karna hai ok
quiz = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Paris", "Rome", "Madrid"],
        "answer": "Paris"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Saturn"],
        "answer": "Mars"
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "answer": "Pacific"
    }
]

@app.route('/')
def home():
    # Initialize the session variables
    session['question_index'] = 0  # Start with the first question
    session['score'] = 0  # Reset the score
    session['user_understanding_level'] = user_understanding_level  # Track user understanding level
    return redirect(url_for('quiz_view'))

@app.route('/quiz_view', methods=['GET', 'POST'])
def quiz_view():  # Renamed the function to avoid a conflict with the 'quiz' variable
    global user_understanding_level
    question_index = session.get('question_index', 0)
    
    # If all questions have been answered, show the result
    if question_index >= len(quiz):  # Ensure we're working with the 'quiz' list
        return redirect(url_for('result'))

    # Get the current question
    question = quiz[question_index]

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        correct_answer = question['answer']

        # Retrieve the user's current understanding level from session
        user_understanding_level = session.get('user_understanding_level', 0.5)
        question_difficulty_value = question_difficulty[question_index]

        # If the answer is correct
        if user_answer == correct_answer:
            session['score'] += 1  # Increment score

            # Update the understanding level if correct
            user_understanding_level_new = user_understanding_level + (1 - user_understanding_level) * question_difficulty_value * 0.1
            session['user_understanding_level'] = user_understanding_level_new
            user_understanding_level = user_understanding_level_new

            session['question_index'] += 1  # Move to the next question
            return redirect(url_for('quiz_view'))  # Load the next question
        else:
            # Flash a message for incorrect answer
            flash("Incorrect answer. Please try again.")
            
            # Update the understanding level if incorrect
            user_understanding_level_new = user_understanding_level + (0 - user_understanding_level) * question_difficulty_value * 0.1
            session['user_understanding_level'] = user_understanding_level_new
            user_understanding_level = user_understanding_level_new

    return render_template('quiz.html', question=question)

@app.route('/result')
def result():
    global user_understanding_level
    score = session.get('score', 0)
    total = len(quiz)  # Ensure we're calculating the total correctly from the 'quiz' list
    user_understanding_level = session.get('user_understanding_level', 0.5)
    return render_template('result.html', score=score, total=total, user_understanding_level=user_understanding_level)

if __name__ == '__main__':
    app.run(debug=True)
