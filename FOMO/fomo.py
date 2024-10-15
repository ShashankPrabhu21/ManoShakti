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
    return render_template('fomo.html')

@app.route('/submit', methods=['POST'])
def submit():
    student_id = request.form['student_id']
    student_name = request.form['student_name']
    
    # Capture responses for all the questions
    responses = {f'q{i}': request.form[f'q{i}'] for i in range(1, 11)}
    fomo_score = sum(int(responses[f'q{i}']) for i in range(1, 11))

    # Categorize the level of FoMO
    if fomo_score <= 20:
        fomo_level = "Low"
    elif fomo_score <= 30:
        fomo_level = "Moderate"
    elif fomo_score <= 40:
        fomo_level = "High"
    else:
        fomo_level = "Extreme"

    # Save the data to Firestore
    doc_ref = db.collection('fomo_responses').document(student_id)
    doc_ref.set({
        'student_name': student_name,
        'student_id': student_id,
        'question_responses': responses,  # Save all questions as a map
        'fomo_score': fomo_score,
        'fomo_level': fomo_level
    })

    # Render the result after submission
    return render_template('result.html', fomo_score=fomo_score, fomo_level=fomo_level)

if __name__ == '__main__':
    app.run(debug=True)
