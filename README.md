Quizify - AI-Powered MCQ Generator
<!-- Replace with a URL to a screenshot of your app -->

Quizify is a smart web application that transforms your PDF study materials into interactive multiple-choice quizzes. Powered by the Google Gemini API, it reads any uploaded PDF and automatically generates a set of questions, allowing you to test your knowledge in a fun and engaging way.

Features
PDF to Quiz: Upload any PDF document (lecture notes, book chapters, articles) and instantly get a quiz.

AI-Powered Questions: Leverages the Google Gemini API to generate relevant and challenging multiple-choice questions.

Interactive Interface: Take the quiz directly in your browser with a clean and modern UI.

Instant Scoring: Get your score immediately after submission, with a detailed review of your answers.

Built With
This project is built with a modern tech stack:

Backend: Python with the Flask framework.

AI Model: Google Gemini API (gemini-1.5-flash-latest).

PDF Parsing: PyMuPDF.

Frontend: HTML5, CSS3, and Jinja2 templating.

Getting Started
Follow these instructions to get a copy of the project up and running on your local machine.

Prerequisites
You need to have Python 3.7+ and pip installed on your system.

Installation
Clone the Repository

git clone https://github.com/your-username/quizify.git
cd quizify

Create a Virtual Environment (Recommended)

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install Dependencies
Install all the necessary packages from the requirements.txt file.

pip install -r requirements.txt

Set Up Your API Key

Get your free Gemini API key from Google AI Studio.

In the root of your project folder, create a file named .env.

Add your API key to the .env file like this:

GEMINI_API_KEY=AIzaSy...your...key...here

Running the Application
Run the Flask server from the root of your project folder:

python app.py

Open your web browser and navigate to http://127.0.0.1:5000/.

File Structure
Here is the layout of the project:

/quizify
├── .env                  # Stores your secret API key
├── app.py                # The main Flask application logic
├── requirements.txt      # Lists all Python dependencies
├── static/
│   └── style.css         # All the CSS styling
└── templates/
    ├── index.html        # The main upload page
    ├── quiz.html         # The page where the user takes the quiz
    └── results.html      # The page that displays the final score

License
Distributed under the MIT License. See LICENSE for more information.


