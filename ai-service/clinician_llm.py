import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_clinician_note(probabilities, priority, confidence_level):
    prompt = f"""
You are an expert radiologist.

AI Probabilities:
{json.dumps(probabilities, indent=2)}

Triage Priority: {priority}
AI Confidence Level: {confidence_level}

Write a structured clinician note including:
- Impression
- Interpretation
- Risk discussion
- Recommendation
- Do not add patient name in note and other unnecessary things like title.

Be professional and concise.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]

def answer_medical_question(question):
    prompt = f"""
You are a clinical AI assistant.
Answer the following medical question clearly and safely:

{question}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]