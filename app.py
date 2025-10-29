from flask import Flask, render_template, request, jsonify
import json, random, os
from emotion_model import detect_emotion

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "your_secret_key")

# Load dataset
with open('dataset.json', 'r', encoding='utf-8') as f:
    music_data = json.load(f)

# Store conversation states (per session)
user_states = {}

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
    data = request.json
    user_input = data.get('message', '').strip().lower()
    session_id = data.get('session', 'default')

    # Ensure a state exists for this session
    if session_id not in user_states:
        user_states[session_id] = {
            "emotion": None,
            "awaiting_consent": False,
            "awaiting_selection": False,
            "song_choices": []
        }

    state = user_states[session_id]

    # --- Consent step ---
    if state["awaiting_consent"]:
        emotion = state["emotion"]
        state["awaiting_consent"] = False

        if user_input == 'y':
            songs = random.sample(music_data[emotion], 3)
            state["song_choices"] = songs
            state["awaiting_selection"] = True

            response = "Here are 3 songs for your mood:\n"
            for i, song in enumerate(songs, 1):
                response += f"{i}. {song['title']} by {song['artist']}\n"
            response += "Reply with 1, 2, or 3 to play your choice."
            return jsonify({"response": response, "link": None})

        elif user_input == 'n':
            return jsonify({"response": advice.get(emotion, "Take care!"), "link": None})

        else:
            state["awaiting_consent"] = True
            return jsonify({"response": "Please reply with 'y' or 'n'. Want a song recommendation?", "link": None})

    # --- Song selection step ---
    if state["awaiting_selection"]:
        if user_input in ['1', '2', '3']:
            index = int(user_input) - 1
            song = state["song_choices"][index]
            state["awaiting_selection"] = False
            return jsonify({
                "response": f"Great choice! Here's {song['title']} by {song['artist']}",
                "link": song['url']
            })
        else:
            return jsonify({"response": "Please reply with 1, 2, or 3 to choose a song.", "link": None})

    # --- Emotion detection step ---
    emotion = detect_emotion(user_input)
    state["emotion"] = emotion
    state["awaiting_consent"] = True

    return jsonify({
        "response": f"I sense you're feeling {emotion}. Want me to recommend a song for you? (y/n)",
        "link": None
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
