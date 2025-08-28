import os
import google.generativeai as genai
from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv
import fitz  # PyMuPDF
import json

# Load environment variables from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Flask app
app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    """Renders the main upload page."""
    return render_template('index.html')

# Route to handle PDF upload and MCQ generation
@app.route('/upload', methods=['POST'])
def upload_pdf():
    """Handles file upload, extracts text, and generates MCQs using Gemini API."""
    if 'pdf' not in request.files:
        return "No file part", 400
    file = request.files['pdf']
    if file.filename == '':
        return "No selected file", 400

    if file:
        try:
            # 1. Extract text from the uploaded PDF
            pdf_document = fitz.open(stream=file.read(), filetype="pdf")
            text = ""
            for page in pdf_document:
                text += page.get_text()
            pdf_document.close()

            # 2. Use Gemini model to generate MCQs
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            # THIS PROMPT IS UPDATED TO BE MORE SPECIFIC
            prompt = f"""
            You are an expert MCQ generator. From the following text, create 10 multiple-choice questions (MCQs).
            
            Instructions for question generation:
            1. Each question must have exactly one single correct answer and three plausible but incorrect distractors.
            2. Do NOT create any questions where "All of the above" or similar options are used.
            3. Ensure the output is ONLY a valid JSON array. Each object in the array must have the keys 'question', 'options' (a list of 4 choices), 
            and 'correct_answer'. Do not add any extra text or explanations.

            Here is the text:
            {text}
            """
            
            response = model.generate_content(prompt)
            
            # Clean the response to get a valid JSON string
            clean_json_str = response.text.strip().replace('```json', '').replace('```', '')
            mcqs = json.loads(clean_json_str)

            # 3. Render the quiz page with the generated questions
            return render_template('quiz.html', questions=mcqs)

        except Exception as e:
            print(f"An error occurred: {e}")
            return "An error occurred while generating MCQs. Please try again.", 500

    return redirect(url_for('index'))

# Route to handle quiz submission and scoring
@app.route('/submit', methods=['POST'])
def submit_quiz():
    """Processes the submitted quiz answers and displays the results."""
    user_answers = request.form
    questions_data_str = user_answers.get('questions_data')
    
    if not questions_data_str:
        return redirect(url_for('index'))

    questions = json.loads(questions_data_str)
    
    score = 0
    results_data = []

    # Compare user answers with correct answers
    for i, question in enumerate(questions, 1):
        user_answer = user_answers.get(f'question_{i}')
        correct_answer = question['correct_answer']
        
        is_correct = False # Default to incorrect
        # THIS BLOCK IS THE FIX
        # First, check if the user actually answered the question
        if user_answer:
            # If they did, clean both strings and compare them
            is_correct = (user_answer.strip().strip('.').strip() == correct_answer.strip().strip('.').strip())
        
        if is_correct:
            score += 1
        
        results_data.append({
            'question': question['question'],
            'user_answer': user_answer or "No answer", # Show "No answer" if skipped
            'correct_answer': correct_answer,
            'is_correct': is_correct
        })

    total_questions = len(questions)
    
    # Render the results page with the score and detailed feedback
    return render_template('results.html', 
                           score=score, 
                           total_questions=total_questions,
                           results=results_data)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
