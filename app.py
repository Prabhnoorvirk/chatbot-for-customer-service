import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = 'AIzaSyCZzK39MSn6eupHAUQU_GYGPg42rkQ7dio'
API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent'

@app.route('/')
def chat_page():
    return render_template("chat.html")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')

    print(f"User: {user_message}")

    payload = {
        "contents": [
            {
                "parts": [{"text": user_message}]
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(f"{API_URL}?key={API_KEY}", json=payload, headers=headers)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")

        if response.status_code == 200:
            response_data = response.json()
            parts = response_data['candidates'][0]['content']['parts']
            bot_reply = parts[0]['text'] if parts else "No reply received."
        else:
            bot_reply = f"Error: {response.status_code}"

    except Exception as e:
        print(f"Error: {e}")
        bot_reply = 'Oops! Something went wrong.'

    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
