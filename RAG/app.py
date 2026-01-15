import sys
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# 🔧 Import Updated RAG + Ollama
ROOT = Path(__file__).resolve().parents[0]
sys.path.append(str(ROOT))

from RAG.query_rag import answer_from_rag  # NEW
from Ollama.llm_client import ask_ollama_with_context  # fallback


app = FastAPI(
    title="NIET RAG + Ollama Chat API",
    version="2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str



@app.get("/")
def health():
    return {"status": "RAG Server Running", "version": "2.0"}



@app.post("/chat")
def chat(req: QueryRequest):
    user_query = req.question.strip()
    lowered = user_query.lower()

    
    GREETINGS = {
        "hi": "Hi there! 👋 How can I assist you today?",
        "hello": "Hello! 😊 What would you like to know about NIET?",
        "hey": "Hey! 👋 I'm here to help with your NIET queries!",
        "good morning": "Good morning ☀️ How can I help you today?",
        "good afternoon": "Good afternoon 🌞 What information do you need?",
        "good evening": "Good evening 🌙 How may I assist you?",
        "namaste": "Namaste 🙏 How may I help you?",
        "hola": "Hola! 👋 How can I support you regarding NIET?"
    }

    if lowered in GREETINGS:
        return {
            "source": "greeting",
            "answer": GREETINGS[lowered],
            "context_used": "pure-greeting"
        }

    for g in GREETINGS:
        if lowered.startswith(g + " ") or lowered.startswith(g + ","):
            greeting_text = GREETINGS[g]
            cleaned_query = lowered.replace(g, "").replace(",", "").strip()

            rag_result = answer_from_rag(cleaned_query)

            if rag_result and "not found" not in rag_result.lower():
                return {
                    "source": "rag+greeting",
                    "answer": greeting_text + " " + rag_result,
                    "context_used": "greeting + rag"
                }

            llm = ask_ollama_with_context(cleaned_query, rag_result or "")
            return {
                "source": "ollama+greeting",
                "answer": greeting_text + " " + llm,
                "context_used": "greeting + fallback LLM"
            }

    rag_result = answer_from_rag(lowered)
    fallback = (
        rag_result is None
        or "not found" in rag_result.lower()
        or "no matching" in rag_result.lower()
    )

    if fallback:
        llm = ask_ollama_with_context(lowered, rag_result or "")
        return {
            "source": "ollama",
            "answer": llm,
            "context_used": rag_result or "no rag context"
        }

    return {
        "source": "rag",
        "answer": rag_result,
        "context_used": "rag-match"
    }
