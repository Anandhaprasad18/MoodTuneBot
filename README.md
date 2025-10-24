# MoodTuneBot 

**MoodTuneBot** is an AI-powered chatbot that recommends songs based on your current mood. It uses a Transformer-based emotion detection model (`DistilRoBERTa`) to analyze user messages and suggest relevant music tracks from a curated dataset.

---

## Features

- Detects user emotions in real-time using NLP.
- Suggests 3 song recommendations based on detected mood.
- Handles user interaction with consent and selection flow.
- Supports multiple moods: happy, sad, angry, neutral, motivated, night.
- Interactive frontend with typing indicator and particle effects.

---

## Tech Stack

- **Backend:** Python, Flask
- **ML Model:** Hugging Face Transformers (`j-hartmann/emotion-english-distilroberta-base`)
- **Frontend:** HTML, CSS, JavaScript
- **Hosting:** Render (backend), optional Firebase Hosting (frontend)
- **Dependencies:** See `requirements.txt`

---

## 💾 Installation (Local)

1. Clone the repository:
   ```bash
   git clone https://github.com/Anandhaprasad18/MoodTuneBot.git
   cd MoodTuneBot
