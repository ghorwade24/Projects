from flask import Flask, render_template, request, jsonify
from AI_Chatbot import load_knowledge_base,find_best_match, chat_bot

app = Flask(__name__, template_folder='Template',static_url_path='/static')
knowledge_base = load_knowledge_base("C:/Users/Shekhar/OneDrive/Desktop/Langchain/BE/New folder/knowlaged_base.json")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['user_input']
    bot_response = chat_bot(user_input, knowledge_base)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
