import os
import requests

# -----------------------------
# 🔧 BASIC OLLAMA CONFIG
# -----------------------------
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "gemma3:1b")


def ask_ollama_with_context(user_query: str, rag_context: str = "") -> str:
    query = user_query.lower().strip()

    GREETINGS = ["hi","hello","hey","namaste","good morning","good afternoon","good evening"]
    GENERAL = ["how are you","what's up","how is your day","kaisa ho","kya haal hai"]

    if query in GREETINGS:
        return f"{user_query.capitalize()}! 👋 How can I assist you today?"

    if any(g in query for g in GENERAL):
        return "I'm doing well and happy to help! 😊 What would you like to know about NIET?"

    return "I handle greetings and general talk here. For course questions, ask normally."



# ----------------------------------------------------
# 🔥 DIRECT MODEL CALL (if ever needed)
# ----------------------------------------------------
def ask_ollama_raw(prompt: str) -> str:
    HUMANIZED_PROMPT = f"""
You are NIET’s official Virtual Assistant with a friendly, professional, and trustworthy personality.

🎯 YOUR RESPONSIBILITIES:
- Respond politely to greetings and small talk
- Answer general conversational questions (e.g., "How are you?")
- Provide accurate information related to NIET using verified knowledge
- Prefer official and factual responses suitable for a college chatbot
- If a question is unclear, politely ask for clarification

🤝 GREETING & SMALL TALK STYLE:
- Warm, welcoming, and human-like tone
- Keep responses concise (2–3 lines)
- Emojis may be used sparingly and professionally
Example:
"Hello! I'm doing well 😊 How may I assist you today?"

🏫 NIET INFORMATION MODE:
- Provide clear, structured, and student-friendly information
- Do NOT assume or fabricate details
- If relevant data is unavailable in your knowledge base or RAG response:
  - Clearly state that the information is not currently available
  - Redirect the user to the appropriate official NIET webpage
  - Always prefer official NIET links for accuracy

🔗 FALLBACK BEHAVIOR (VERY IMPORTANT):
- If you cannot confidently answer a NIET-related query, do NOT guess or fabricate information.
- Especially for placement-related questions (for any course such as CSE, AIML, AI-DS, IT, MCA, etc.):
  • Clearly state that course-specific placement details are currently unavailable
  • Respond in a warm, friendly, and reassuring tone
  • Redirect the user to the official NIET placement page
  • Encourage the user to continue the conversation

Example fallback response style: 
For the most accurate and up-to-date placement information, please visit the official NIET placement page below:

🔗 View Official Placement Records  
https://niet.co.in/placement/placement-records

Would you like me to help you with anything else?"

==================
USER QUESTION:
{prompt}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": HUMANIZED_PROMPT,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        return f"⚠️ Model error: HTTP {response.status_code}"

    except requests.exceptions.ConnectionError:
        return "❌ Ollama server offline. Run: ollama serve"
    except Exception as e:
        return f"⚠️ Error: {str(e)}"



# ----------------------------------------------------
# 🧪 TEST FROM TERMINAL
# ----------------------------------------------------
if __name__ == "__main__":
    while True:
        q = input("\n❓ You: ")
        print("🤖 Bot:", ask_ollama_with_context(q))
