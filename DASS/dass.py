from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate('../firebase_credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Function to determine DASS level
def get_depression_level(score):
    if score >= 28:
        return 'Extremely Severe'
    elif 21 <= score <= 27:
        return 'Severe'
    elif 14 <= score <= 20:
        return 'Moderate'
    elif 10 <= score <= 13:
        return 'Mild'
    else:
        return 'Normal'

def get_anxiety_level(score):
    if score >= 20:
        return 'Extremely Severe'
    elif 15 <= score <= 19:
        return 'Severe'
    elif 10 <= score <= 14:
        return 'Moderate'
    elif 8 <= score <= 9:
        return 'Mild'
    else:
        return 'Normal'

def get_stress_level(score):
    if score >= 34:
        return 'Extremely Severe'
    elif 26 <= score <= 33:
        return 'Severe'
    elif 19 <= score <= 25:
        return 'Moderate'
    elif 15 <= score <= 18:
        return 'Mild'
    else:
        return 'Normal'

# Placeholder function for FoMO level calculation
def get_fomo_level(fomo_score):
    # Add your logic to calculate FoMO score here
    return 'FoMO Level Placeholder'

@app.route('/')
def home():
    return render_template('dass.html')

@app.route('/submit', methods=['POST'])
def submit():
    student_id = request.form['student_id']
    student_name = request.form['student_name']

    # Collecting responses for DASS questions
    responses = {f'q{i}': int(request.form[f'q{i}']) for i in range(1, 22)}  

    # Calculate the scores based on specific questions
    depression_score = sum(responses[f'q{i}'] for i in [3, 5, 10, 13, 16, 17, 21]) * 2
    anxiety_score = sum(responses[f'q{i}'] for i in [2, 4, 7, 9, 15, 19, 20]) * 2
    stress_score = sum(responses[f'q{i}'] for i in [1, 6, 8, 11, 12, 14, 18]) * 2

    # Determine the levels
    depression_level = get_depression_level(depression_score)
    anxiety_level = get_anxiety_level(anxiety_score)
    stress_level = get_stress_level(stress_score)


    
    doc_ref = db.collection('dass_responses').document(student_id)
    doc_ref.set({
        'student_name': student_name,
        'student_id': student_id,
        'question_responses': responses, 
        'depression_score': depression_score,
        'depression_level': depression_level,
        'anxiety_score': anxiety_score,
        'anxiety_level': anxiety_level,
        'stress_score': stress_score,
        'stress_level': stress_level
    })

    return render_template('result.html',depression_level= depression_level,anxiety_level=anxiety_level,stress_level=stress_level)

if __name__ == '__main__':
    app.run(debug=True)
