from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

questions = [
    {"question": "What is the capital of France?", "options": ["Paris", "London", "Berlin", "Madrid"], "answer": "Paris", "category": "general"},
    {"question": "Who invemted Light Bulb?", "options": ["Nikola Tesla", "Thomas Edison", "Alexander Graham Bell", "Albert Einstein"], "answer": "Thomas Edison", "category": "general"},
    {"question": "Which planet is known as Red Planet?", "options": ["Venus", "Jupiter", "Mars", "Saturn"], "answer": "Mars", "category": "general"},
    {"question": "Which is the largest ocean?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "answer": "Pacific", "category": "general"},
    {"question": "Who wrote the play 'Romeo and Juliet'?", "options": ["William Shakespeare", "Charles Dickens", "Mark Twain", "Jane Austen"], "answer": "William Shakespeare", "category": "general"},
    
    {"question": "What is the correct file extension for python files?", "options": [".py", ".java", ".cpp", ".txt"], "answer": ".py", "category": "python"},
    {"question": "Which keyword is used to define a function in python?", "options": ["func", "def", "define", "function"], "answer": "def", "category": "python"},
    {"question": "What is the output of print(2 * 3 ** 2)?", "options": ["18", "36", "12", "9"], "answer": "18", "category": "python"},
    {"question": "Which data type is immutable in Python?", "options": ["list", "dictionary", "set", "tuple"], "answer": "tuple", "category": "python"},
    {"question": "What will len('Hello') return?", "options": ["4", "5", "6", "0"], "answer": "5", "category": "python"},

    {"question": "What is 15 + 7?", "options": ["20", "21", "22", "23"], "answer": "22", "category": "math"},
    {"question": "What is the square root of 81?", "options": ["7", "8", "9", "10"], "answer": "9", "category": "math"},
    {"question": "If a triangle has angles of 60° and 90°, what is the third angle?", "options": ["30°", "40°", "50°", "60°"], "answer": "30°", "category": "math"},
    {"question": "What is the value of π (pi) approximately?", "options": ["2.14", "3.14", "4.14", "5.14"], "answer": "3.14", "category": "math"},
    {"question": "Solve: 5 x (6 - 2)", "options": ["10", "20", "30", "40"], "answer": "20", "category": "math"},

    {"question": "What does 'HTTP' stand for?", "options": ["Hyper Text Transfer Protocol", "High Tech Transfer Protocol", "Hyperlink Transfer Process", "Hyper Text Transmission Protocol"], "answer": "Hyper Text Transfer Protocol", "category": "tech"},
    {"question": "Which company developed the Windows operating system?", "options": ["Apple", "Microsoft", "Google", "IBM"], "answer": "Microsoft", "category": "tech"},
    {"question": "What is the main function of a CPU?", "options": ["Store Data", "Display Graphics", "Process Instructions", "Manage memory"], "answer": "Process Instructions", "category": "tech"},
    {"question": "Which device is used to convert digital signals into analog signals for communication?", "options": ["Router", "Switch", "Modem", "Hub"], "answer": "Modem", "category": "tech"},
    {"question": "What does 'AI' stand for in technology?", "options": ["Automated Integration", "Artificial Intelligence", "Advanced Internet", "Applied Information"], "answer": "Artificial Intelligence", "category": "tech"}
]

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
def default():
    return redirect(url_for('home'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'category_questions' not in session:
        return redirect(url_for('home'))  # Redirect to home if no category is selected
    
    question_index = session.get('question_index', 0)
    category_questions = session['category_questions']
    
    if question_index >= len(category_questions):
        return redirect(url_for('results'))
    
    question = category_questions[question_index]
    return render_template('quiz.html', question=question, index=question_index, total=len(category_questions))

@app.route('/submit', methods=['POST'])
def submit():
    if 'question_index' not in session or 'answers' not in session:
        return redirect(url_for('restart'))  # Restart if session data is missing
    
    question_index = session.get('question_index', 0)
    
    if 'category_questions' in session:
        questions_to_use = session['category_questions']
    else:
        questions_to_use = questions
    
    if question_index >= len(questions_to_use):  # Prevent out-of-range errors
        return redirect(url_for('results'))
    
    selected_option = request.form.get('option', '')  # Handle missing form input safely
    correct_answer = questions_to_use[question_index]['answer']
    
    session['answers'].append({
        'question': questions_to_use[question_index]['question'],
        'selected': selected_option,
        'correct': correct_answer
    })
    if selected_option == correct_answer:
        session['score'] = session.get('score', 0) + 1
    
    session['question_index'] = question_index + 1
    
    return redirect(url_for('quiz'))

@app.route('/previous', methods=['GET'])
def previous():
    if 'question_index' in session and session['question_index'] > 0:
        session['question_index'] -= 1  # Decrease the question index
        session['answers'].pop()  # Remove the last answer to allow re-selection
    return redirect(url_for('quiz'))

@app.route('/results')
def results():
    return render_template('results.html', score=session['score'], answers=session['answers'])

@app.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('quiz'))

@app.route('/category/<category_name>')
def category(category_name):
    # Filter questions based on the selected category
    category_questions = [q for q in questions if q['category'] == category_name]
    if not category_questions:
        return redirect(url_for('home'))  # Redirect to home if no questions in the category
    
    session['category_questions'] = category_questions[:5]  # Limit to 5 questions
    session['question_index'] = 0
    session['score'] = 0
    session['answers'] = []
    
    return redirect(url_for('quiz'))

if __name__ == '__main__':
    app.run(debug=True)
