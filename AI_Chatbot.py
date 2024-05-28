from flask import Flask, render_template, request
import json
import re
from difflib import get_close_matches

app = Flask(__name__, template_folder='Template',static_url_path='/static')

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def preprocess_question(user_question: str) -> str:
    user_question = re.sub(r'\b(what is|explain|define|how to)\b', '', user_question, flags=re.IGNORECASE)
    user_question = user_question.strip(' ?.,!')
    return user_question

def find_best_match(user_question: str, questions) -> str | None:
    if isinstance(questions, dict):
        matches = get_close_matches(user_question, questions.keys(), n=1, cutoff=0.6)
    elif isinstance(questions, list):
        matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    else:
        raise TypeError("Expected 'questions' to be either a dictionary or a list")
    
    return matches[0] if matches else None

def chat_bot(user_input: str, knowledge_base: dict):
    user_question = preprocess_question(user_input)
    best_match: str | None = find_best_match(user_question, knowledge_base["questions"])
    
    if best_match:
        answer: str = knowledge_base["questions"][best_match]
        return answer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/response', methods=['POST'])
def response():
    knowledge_base = load_knowledge_base("knowlaged_base.json")
    user_input = request.form['user_input']
    response_text = chat_bot(user_input, knowledge_base)
    print("User's Question:", user_input)
    print("Chatbot's Response:", response_text)
    return render_template('index.html', user_question=user_input,response=response_text)

if __name__ == '__main__':
    app.run(debug=True)
