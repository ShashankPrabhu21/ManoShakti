from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate('../firebase_credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def home():
    return render_template('adhd.html')

@app.route('/submit', methods=['POST'])
def submit():
    student_id = request.form['student_id']
    student_name = request.form['student_name']
    
    # Capture responses for all the questions (assumes responses are strings that can be converted to int)
    responses = {f'q{i}': int(request.form[f'q{i}']) for i in range(1, 19)}  # Ensure responses are integers

    # Calculate Part A score: count how many responses in the first 6 questions (q1 to q6) are 3 or above
    parta_score = sum(1 for i in range(1, 7) if responses[f'q{i}'] >= 3)
    
    # Calculate Part B score: count how many responses in the last 12 questions (q7 to q18) are 3 or above
    partb_score = sum(1 for i in range(7, 19) if responses[f'q{i}'] >= 3)

    # Calculate subscale scores using the appropriate question indices
    inattentive_subscale_score = sum(responses[f'q{i}'] for i in [1, 2, 3, 4, 7, 8, 9, 10])  # Ensure correct indices
    motor_impulsive_subscale_score = sum(responses[f'q{i}'] for i in [5, 6, 11, 12, 13])  # Ensure correct indices
    verbal_impulsive_subscale_score = sum(responses[f'q{i}'] for i in [14, 15, 16, 17])  # Ensure correct indices

    # Calculate total score (if necessary)
    total_score = parta_score + partb_score

    # Save the data to Firestore
    doc_ref = db.collection('adhd_responses').document(student_id)
    doc_ref.set({
        'student_name': student_name,
        'student_id': student_id,
        'question_responses': responses,  # Save all questions as a map
        'parta_score': parta_score,
        'partb_score': partb_score,
        'inattentive_subscale_score': inattentive_subscale_score,
        'motor_impulsive_subscale_score': motor_impulsive_subscale_score,
        'verbal_impulsive_subscale_score': verbal_impulsive_subscale_score,
        'total_score': total_score  # Optional: Save total score if needed
    })

    return render_template('result.html', total_score=total_score, parta_score=parta_score,partb_score=partb_score,inattentive_subscale_score=inattentive_subscale_score,motor_impulsive_subscale_score=motor_impulsive_subscale_score,verbal_impulsive_subscale_score=verbal_impulsive_subscale_score)

if __name__ == '__main__':
    app.run(debug=True)


