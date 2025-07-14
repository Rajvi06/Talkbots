from flask import Flask, render_template, request, jsonify

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    return get_Chat_response(input)

@app.route("/chat", methods=["POST"])
def chats():
    msg = request.json.get("msg")  # Get the message from JSON payload
    response = get_chat_response(msg)  # Generate response
    return jsonify({"response": response})  # Return as JSON

@app.route("/chat", methods=["POST"])
def chatss():
    msg = request.json.get("msg")
    response = generate_response(msg)
    return jsonify({"response": response})

def generate_response(input_text):
    input_ids = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors="pt")
    chat_history_ids = model.generate(input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response

def get_chat_response(text):
    # Chat response generation logic
    new_user_input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors="pt")
    chat_history_ids = model.generate(new_user_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(chat_history_ids[:, new_user_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response

def get_Chat_response(text):

    for step in range(5):
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = tokenizer.encode(str(text) + tokenizer.eos_token, return_tensors='pt')

        # append the new user input tokens to the chat history
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

        # generated a response while limiting the total chat history to 1000 tokens, 
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

        # pretty print last ouput tokens from bot
        return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)


if __name__ == '__main__':
    app.run(port=5000)
