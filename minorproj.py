import datetime
import hashlib
from flask import *
from mongo import MongoDBHelper

web_app = Flask("ProfessionPilot")

@web_app.route("/")
def index():
    return render_template('login.html')

@web_app.route("/")
def quiz():
    return render_template('quizpage.html')

@web_app.route("/register")
def register():
    return render_template('register.html')

@web_app.route("/about")
def about():
    return render_template('about.html')


@web_app.route("/home")
def home():
    return render_template('index.html')

@web_app.route("/matriculation")
def matriculation():
    return render_template('matriculation.html')

@web_app.route("/class")
def classes():
    return render_template('/class.html')

@web_app.route("/register-person", methods=['POST'])
def register_person():
    person_data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'password': hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest(),
        'createdon': datetime.datetime.today()
    }
    print(person_data)
    db = MongoDBHelper(collection="professionpilot")
    # Update MongoDB Helper insert function, to return result here
    result = db.insert(person_data)

    # Test the same
    person_id = result.inserted_id
    session['person_id'] = str(person_id)
    session['person_name'] = person_data['name']
    session['person_email'] = person_data['email']
    return render_template('login.html')

@web_app.route("/login-person", methods=['POST'])
def login_person():
    person_data = {
        'email': request.form['email'],
        'password': hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest(),
    }
    print(login_person)
    db = MongoDBHelper(collection="professionpilot")
    documents = db.fetch(person_data)
    print(documents, type(documents))

    if len(documents) == 1:
        session['person_id'] = str(documents[0]['_id'])
        session['person_email'] = documents[0]['email']
        session['person_name'] = documents[0]['name']
        print(vars(session))
        return render_template('index.html', email=session['person_email'], name=session['person_name'])
    else:
        return render_template('errors.html', message="Invalid Login!!! Login Again??")
#HTML Questions Start---
quiz_questions = [
    {
        'question_number': 1,
        'q1': 'What is the chemical symbol for oxygen? -',
        'options': ['Ox', ' O2', 'O', 'Ox2'],
        'correct_answer': 'O'
    },
    {
        'question_number': 2,
        'q1': 'Who is often referred to as the "Father of Modern Physics"? -',
        'options': [' Isaac Newton', 'Albert Einstein', 'Galileo Galilei', 'Thomas Edison'],
        'correct_answer': 'Albert Einstein'
    },
    {

        'question_number': 3,
        'q1': 'Which planet is known as the "Red Planet"?',
        'options': ['Earth', 'Mars', 'Jupiter', 'Venus'],
        'correct_answer': 'Mars'
    },
    {
        'question_number': 4,
        'q1': 'What is the largest organ in the human body?',
        'options': ['Brain', 'Heart', 'Skin', 'Liver'],
        'correct_answer': 'Skin'
    },
    {
        'question_number': 5,
        'q1': 'Which of the following is a renewable source of energy?',
        'options': ['Natural Gas','Coal', 'Petroleum', 'Solar Power'],
        'correct_answer': 'Solar Power'
    },
    {
        'question_number': 6,
        'q1': 'What is the chemical formula for water?  ',
        'options': ['H2O', 'CO2', 'NH2', 'H2'],
        'correct_answer': 'H20'
    },
    {
        'question_number': 7,
        'q1': 'What is the primary purpose of financial accounting?',
        'options': ['To predict future financial performance', 'To record and report financial transactions', ' To provide information for internal decision-making', 'To manage human resources'],
        'correct_answer': 'To record and report financial transactions'
    },
    {
        'question_number':8,
        'q1': ' Which of the following is not a type of market structure in economics?',
        'options': [' Monopoly', 'Oligopoly', ' Duopoly', 'Monologue'],
        'correct_answer': 'Monologue'
    },
{
        'question_number': 9,
        'q1': 'What does the term "ROI" stand for in the context of finance and investments? -',
        'options': [' Return on Investment', 'Risk of Inflation', ' Rate of Interest', 'Revenue of Income'],
        'correct_answer': ' Return on Investment'
    },
{
        'question_number': 10,
        'q1': 'In the context of international trade, what does "GDP" stand for?',
        'options': [' Global Domestic Product', 'Gross Domestic Profit', 'Gross Domestic Product', 'General Development Plan'],
        'correct_answer': ' Global Domestic Product'
    },
{
        'question_number': 11,
        'q1': 'Who painted the Mona Lisa, one of the most famous works of art in the world?',
        'options': ['Vincent van Gogh', 'Pablo Picasso', ' Leonardo da Vinci', 'Michelangelo'],
        'correct_answer': ' Leonardo da Vinci'
    },
{
        'question_number': 12,
        'q1': 'Which famous playwright wrote "Romeo and Juliet" and "Hamlet"?',
        'options': ['George Bernard Shaw', 'William Shakespeare', 'Anton Chekhov', 'Oscar Wilde'],
        'correct_answer': 'William Shakespeare'
    },
{
        'question_number': 13,
        'q1': 'What literary movement in the 19th century emphasized the importance of individualism, intuition, and the beauty of nature?',
        'options': [' Romanticism', 'Realism', 'Naturalism', ' Symbolism'],
        'correct_answer': ' Romanticism'
    },
{
        'question_number': 14,
        'q1': 'Who is considered the founding figure of modern psychology and wrote "The Interpretation of Dreams"?',
        'options': [' Sigmund Freud', 'Carl Jung', 'Ivan Pavlov', 'B.F. Skinner'],
        'correct_answer': ' Sigmund Freud'
    },
{
        'question_number': 15,
        'q1': 'Which musical style originated in the African American communities of New Orleans and is characterized by improvisation and a strong rhythmic structure?',
        'options': ['Jazz', 'Classical', 'Rock', ' Hip-Hop'],
        'correct_answer': 'Jazz'
    }
    # Add more questions here
]

@web_app.route("/quizpage")
def quizpage():
    return render_template('quizpage.html', quiz_questions=quiz_questions)

@web_app.route("/quizsubmit", methods=['POST'])
def quizsubmit():
    score = 0
    for q1 in quiz_questions:
        selected_answer = request.form.get(q1['q1'])
        if selected_answer == q1['correct_answer']:
            score += 1

    return render_template('quizresult.html', score=score, total=len(quiz_questions), quiz_questions=quiz_questions)

#H  QUIZ Questions End---

def main():
    web_app.secret_key = 'ProfessionPilot-key-1'
    web_app.run(port=5027)

if __name__ == "__main__":
    main()

