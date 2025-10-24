from transformers import pipeline

# Load the emotion detection model
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)

# Map GoEmotions labels to your music categories
def detect_emotion(text):
    result = emotion_classifier(text)[0]
    label = result['label'].lower()

    mapping = {
        'joy': 'happy',
        'amusement': 'happy',
        'excitement': 'happy',
        'pride': 'motivated',
        'desire': 'night',
        'love': 'motivated',
        'gratitude': 'happy',
        'sadness': 'sad',
        'disappointment': 'sad',
        'nervousness': 'night',
        'anger': 'angry',
        'annoyance': 'angry',
        'embarrassment': 'night',
        'neutral': 'neutral',
        'curiosity': 'motivated',
        'realization': 'motivated',
        'sarcasm': 'angry',
        'confusion': 'neutral',
        'fear': 'night'
    }

    return mapping.get(label, 'neutral')
