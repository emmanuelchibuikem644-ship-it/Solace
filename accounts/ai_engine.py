# chatbot_app/ai_engine.py
from transformers import pipeline

# Load the DistilBERT model once when the server starts
# This model identifies: joy, sadness, anger, fear, love, surprise
classifier = pipeline("text-classification", 
                      model="bhadresh-savani/distilbert-base-uncased-emotion", 
                      return_all_scores=True)

def analyze_message(user_text):
    # 1. Detect Emotion (Project Requirement)
    results = classifier(user_text)
    # Sort to find the highest scoring emotion
    top_emotion = max(results[0], key=lambda x: x['score'])
    emotion_label = top_emotion['label']

    # 2. Safety Layer / Crisis Detection (Project Requirement)
    crisis_keywords = ["hurt myself", "suicide", "end my life", "kill myself"]
    if any(word in user_text.lower() for word in crisis_keywords):
        return {
            "response": "I'm concerned about what you're sharing. Please reach out to a professional or a crisis hotline immediately. You are not alone.",
            "emotion": "Crisis",
            "is_safety_alert": True
        }

    # 3. Empathetic Response Logic (Dialogue Manager)
    responses = {
        "joy": "I'm so happy to hear that! What's contributing to this good mood?",
        "sadness": "I'm sorry you're feeling this way. It's okay to feel sad. Want to talk more about it?",
        "anger": "It sounds like you're feeling frustrated. I'm here to listen if you need to vent.",
        "fear": "It’s natural to feel anxious sometimes. Let's take a deep breath together.",
        "surprise": "Wow, that sounds unexpected! How are you processing that?",
        "love": "That sounds like a very warm and positive feeling."
    }

    bot_response = responses.get(emotion_label, "I hear you. Tell me more about that.")
    
    return {
        "response": bot_response, 
        "emotion": emotion_label,
        "is_safety_alert": False
    }