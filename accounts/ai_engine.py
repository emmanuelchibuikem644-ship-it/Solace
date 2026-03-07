# chatbot_app/ai_engine.py
from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="bhadresh-savani/distilbert-base-uncased-emotion",
    return_all_scores=True
)


def analyze_message(user_text):

    user_text_lower = user_text.lower()

    crisis_keywords = [
        "hurt myself",
        "suicide",
        "end my life",
        "kill myself",
        "i want to die",
        "i wish i was dead",
        "life is not worth living",
        "i can't go on"
    ]

    # SAFETY CHECK
    for word in crisis_keywords:
        if word in user_text_lower:
            return {
                "response": "I'm really sorry you're feeling this way. Please reach out to a trusted person or a mental health professional.",
                "emotion": "crisis",
                "is_safety_alert": True
            }

    # EMOTION DETECTION
    results = classifier(user_text)

    # results format: [[{'label':'joy','score':0.9}, ...]]
    emotions = results[0]

    top_emotion = sorted(emotions, key=lambda x: x["score"], reverse=True)[0]

    emotion_label = top_emotion["label"]

    responses = {
        "joy": "I'm really happy to hear that!",
        "sadness": "I'm sorry you're feeling sad. Do you want to talk about it?",
        "anger": "It sounds like you're frustrated. I'm here to listen.",
        "fear": "Feeling anxious can be hard. Tell me more about what's worrying you.",
        "surprise": "That sounds unexpected! How do you feel about it?",
        "love": "That sounds like a warm and positive feeling."
    }

    bot_response = responses.get(
        emotion_label,
        "I understand. Please tell me more."
    )

    return {
        "response": bot_response,
        "emotion": emotion_label,
        "is_safety_alert": False
    }