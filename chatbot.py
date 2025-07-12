from flask import Flask, render_template, request, jsonify
import random
import json
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')

app = Flask(__name__)
lemmatizer = WordNetLemmatizer()

with open("intents.json") as file:
    intents = json.load(file)

def clean_up(sentence):
    words = nltk.word_tokenize(sentence)
    words = [lemmatizer.lemmatize(word.lower()) for word in words]
    return words

def predict_class(sentence):
    sentence_words = clean_up(sentence)
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            pattern_words = clean_up(pattern)
            if all(word in sentence_words for word in pattern_words):
                return intent["tag"]
    return "unknown"

def get_response(tag):
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
    return "Sorry, I don't understand that."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_input = request.form["msg"]
    intent = predict_class(user_input)
    response = get_response(intent)
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)
{
  "intents": [
    {
      "tag": "greeting",
      "patterns": ["hello", "hi", "hey", "good morning"],
      "responses": ["Hey bae!", "Hello there!", "Hi cutie 💖"]
    },
    {
      "tag": "bye",
      "patterns": ["bye", "see you", "goodbye"],
      "responses": ["Bye bae!", "Catch you later 💫", "Bye, have a great day!"]
    },
    {
      "tag": "thanks",
      "patterns": ["thanks", "thank you", "tysm"],
      "responses": ["You're always welcome bae 💋", "Anytime sweetie 😘"]
    },
    {
      "tag": "unknown",
      "patterns": [],
      "responses": ["Uhh... I didn’t get that 😅", "Hmm... can you say it differently?"]
    }
  ]
}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>SmartBot 💬</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <div class="chatbox">
    <div id="chat"></div>
    <form id="chat-form">
      <input type="text" id="msg" placeholder="Type your message..." autocomplete="off" required>
      <button>Send</button>
    </form>
  </div>

  <script>
    const form = document.getElementById("chat-form");
    const chat = document.getElementById("chat");

    form.onsubmit = async (e) => {
      e.preventDefault();
      const msg = document.getElementById("msg").value;
      chat.innerHTML += `<div class='user'>You: ${msg}</div>`;
      document.getElementById("msg").value = "";

      const res = await fetch("/get", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `msg=${msg}`
      });
      const data = await res.json();
      chat.innerHTML += `<div class='bot'>Bot: ${data.reply}</div>`;
    };
  </script>
</body>
</html>
body {
  background: #f8f0ff;
  font-family: 'Segoe UI', sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.chatbox {
  background: white;
  padding: 20px;
  border-radius: 20px;
  width: 400px;
  box-shadow: 0 0 20px rgba(0,0,0,0.1);
}

#chat {
  height: 300px;
  overflow-y: auto;
  margin-bottom: 10px;
}

.user {
  text-align: right;
  color: #000;
  margin: 5px 0;
}

.bot {
  text-align: left;
  color: #9900cc;
  margin: 5px 0;
}

form {
  display: flex;
}

input {
  flex: 1;
  padding: 10px;
  border-radius: 10px 0 0 10px;
  border: 1px solid #ddd;
}

button {
  background: #9900cc;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 0 10px 10px 0;
  cursor: pointer;
}
flask
nltk
