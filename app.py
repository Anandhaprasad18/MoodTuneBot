from flask import Flask, render_template, request, jsonify, session
import json, random
from emotion_model import detect_emotion
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "your_secret_key")

with open('dataset.json', 'r', encoding='utf-8') as f:
    music_data = json.load(f)

advice = {
    "happy": "Keep smiling and spread the joy!",
    "sad": "It's okay to feel down. Take a walk or talk to a friend.",
    "angry": "Take a deep breath. Maybe some quiet time will help.",
    "neutral": "Balance is beautiful. Enjoy the calm.",
    "motivated": "Keep pushing forward. You're doing great!",
    "night": "Unwind and relax. Let the music soothe you."
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message'].strip().lower()

    if session.get('awaiting_consent'):
        emotion = session.get('emotion')
        session['awaiting_consent'] = False

        if user_input == 'y':
            songs = random.sample(music_data[emotion], 3)
            session['song_choices'] = songs
            session['awaiting_selection'] = True
            response = "Here are 3 songs for your mood:\n"
            for i, song in enumerate(songs, 1):
                response += f"{i}. {song['title']} by {song['artist']}\n"
            response += "Reply with 1, 2, or 3 to play your choice."
            return jsonify({"response": response, "link": None})

        elif user_input == 'n':
            return jsonify({"response": advice.get(emotion, "Take care!"), "link": None})
        else:
            session['awaiting_consent'] = True
            return jsonify({"response": "Please reply with 'y' or 'n'. Want a song recommendation?", "link": None})

    if session.get('awaiting_selection'):
        if user_input in ['1', '2', '3']:
            index = int(user_input) - 1
            song = session['song_choices'][index]
            session['awaiting_selection'] = False
            return jsonify({
                "response": f"Great choice! Here's {song['title']} by {song['artist']}",
                "link": song['url']
            })
        else:
            return jsonify({"response": "Please reply with 1, 2, or 3 to choose a song.", "link": None})

    emotion = detect_emotion(user_input)
    session['emotion'] = emotion
    session['awaiting_consent'] = True

    return jsonify({
        "response": f"I sense you're feeling {emotion}. Want me to recommend a song for you? (y/n)",
        "link": None
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)


