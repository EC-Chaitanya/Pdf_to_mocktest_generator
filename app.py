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

            # Limit text length to avoid token limits
            if len(text) > 30000:
                text = text[:30000]

            # 2. Use Gemini 2.5 Flash model (fast and efficient)
            model = genai.GenerativeModel('gemini-flash-lite-latest')
            
            prompt = f"""
            Based on the following text, generate exactly 10 multiple-choice questions (MCQs).
            
            IMPORTANT: Your entire response MUST be a single, valid JSON array. Each object in the array
            must contain three keys: "question", "options" (which is a list of 4 strings), and "correct_answer".
            Do not include any text, explanations, or markdown formatting like ```json before or after the array.

            Text:
            {text}
            """
            
            response = model.generate_content(prompt)
            
            clean_text = response.text
            start = clean_text.find('[')
            end = clean_text.rfind(']')
            if start != -1 and end != -1:
                clean_json_str = clean_text[start:end+1]
                mcqs = json.loads(clean_json_str)
            else:
                raise ValueError("Valid JSON array not found in API response.")

            return render_template('quiz.html', questions=mcqs)

        except Exception as e:
            print(f"An error occurred: {e}") 
            return f"An error occurred while generating MCQs: {str(e)}", 500

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
            # This now handles extra whitespace and trailing periods.
            is_correct = (user_answer.strip().rstrip('.').strip() == correct_answer.strip().rstrip('.').strip())
        
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