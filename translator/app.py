from flask import Flask, request, jsonify, render_template_string
from googletrans import Translator
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  
translator = Translator()

# HTML template for the homepage
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot Translator</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        /* CSS styling */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Roboto', sans-serif; background: linear-gradient(to right, #56ccf2, #2f80ed); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; color: #333; }
        .container { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1); max-width: 600px; width: 100%; }
        .chatbot-header { display: flex; align-items: center; margin-bottom: 20px; }
        .chatbot-header img { width: 60px; height: 60px; border-radius: 50%; margin-right: 15px; }
        .chatbot-header h1 { font-size: 1.5rem; font-weight: 700; color: #333; }
        .chat-window { background-color: #f9f9f9; padding: 20px; border-radius: 15px; height: 300px; overflow-y: auto; margin-bottom: 20px; border: 1px solid #eee; }
        .bot-message, .user-message { display: flex; margin-bottom: 10px; }
        .bot-message { justify-content: flex-start; }
        .user-message { justify-content: flex-end; }
        .message-content { max-width: 80%; padding: 10px 15px; border-radius: 10px; font-size: 1rem; }
        .bot-message .message-content { background-color: #e1f5fe; color: #333; }
        .user-message .message-content { background-color: #2f80ed; color: white; }
        input, select, button { padding: 15px; width: 100%; margin-bottom: 20px; border: none; border-radius: 5px; font-size: 1rem; }
        input, select { background-color: #f2f2f2; }
        button { background-color: #2f80ed; color: white; cursor: pointer; transition: background-color 0.3s ease; }
        button:hover { background-color: #1b5bbf; }
        .loader { display: none; border: 4px solid #f3f3f3; border-radius: 50%; border-top: 4px solid #3498db; width: 30px; height: 30px; animation: spin 1s linear infinite; margin: 20px auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @media(max-width: 600px) { .chatbot-header h1 { font-size: 1.2rem; } input, select, button { font-size: 0.9rem; padding: 12px; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="chatbot-header">
            <img src="https://st5.depositphotos.com/4226061/62815/v/450/depositphotos_628153918-stock-illustration-robot-head-icon-circle-chatbot.jpg" alt="Chatbot">
            <h1>Translator Bot</h1>
        </div>
        <div id="chatWindow" class="chat-window">
            <div class="bot-message">
                <div class="message-content">Hello! I'm your translator bot. Type something to translate!</div>
            </div>
        </div>
        <input type="text" id="userText" placeholder="Enter text to translate" />
        <select id="target_language" name="target_language" required>
            <!-- Language options -->
            <option value="es">Spanish</option>
            <option value="fr">French</option>
            <option value="de">German</option>
            <option value="hi">Hindi</option>
            <option value="zh-cn">Chinese (Simplified)</option>
            <option value="ja">Japanese</option>
            <option value="ru">Russian</option>
            <option value="ar">Arabic</option>
            <option value="pt">Portuguese</option>
            <option value="it">Italian</option>
            <option value="ko">Korean</option>
            <option value="nl">Dutch</option>
            <option value="tr">Turkish</option>
            <option value="pl">Polish</option>
            <option value="sv">Swedish</option>
            <option value="no">Norwegian</option>
            <option value="fi">Finnish</option>
            <option value="he">Hebrew</option>
            <option value="ur">Urdu</option>
            <option value="bn">Bengali</option>
            <option value="ta">Tamil</option>
            <option value="te">Telugu</option>
            <option value="gu">Gujarati</option>
        </select>
        <button onclick="translateText()">Translate</button>
        <div class="loader" id="loader"></div>
    </div>
    <script src="/static/script.js"></script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(html_template)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text')
    target_language = data.get('target_language')
    try:
        translated = translator.translate(text, dest=target_language)
        return jsonify(translated_text = translated.text)
    except Exception as e:
        return jsonify(error = str(e)), 500

if __name__ == '__main__':
    app.run(port=5002, debug=True)
