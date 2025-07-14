from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load the knowledge base from the JSON file
with open('knowledge_base.json', 'r') as f:
    knowledge_base = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message').lower()

    # Search for the message in the knowledge base
    for qa in knowledge_base["questions"]:
        if qa["question"] == user_message:
            return jsonify({"response": qa["answer"]})

    # If no matching response, provide a default response
    return jsonify({"response": "I don't know the answer. Can you tell me?"})

@app.route('/learn', methods=['POST'])
def learn():
    data = request.get_json()
    question = data.get('question').lower()
    answer = data.get('answer')

    # Add the new question and answer to the knowledge base
    knowledge_base["questions"].append({"question": question, "answer": answer})

    # Save the updated knowledge base to the JSON file
    with open('knowledge_base.json', 'w') as f:
        json.dump(knowledge_base, f, indent=4)

    return jsonify({"response": "Thank you! I've learned something new."})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
