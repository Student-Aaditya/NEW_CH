import sys
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

ROOT = Path(__file__).resolve().parents[0]
sys.path.append(str(ROOT))

from RAG.query_rag_2 import answer_rag
from Ollama.llm_client import ask_ollama_with_context
from RAG.router.callback_router import router as callback_router

from router.placement_router import router as placement_router

app = FastAPI(
    title="NIET Chat API",
    version="3.1 - Greeting Only LLM"
)

# 🌐 Allow all origins for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(callback_router, prefix="/api")
app.include_router(placement_router)

class QueryRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"status": "Server Running ✔", "version": "3.1"}

GREETINGS = [
        "hi", "hello", "hey",
        "good morning", "good afternoon",
        "good evening", "namaste"
    ]
SMALL_TALK = [
        "how are you","how r u","how's you","how are u",
        "what's up","sup","how is your day",
        "kya haal hai","kaisa ho","kaise ho","sab theek"
    ]

COURSE_INDICATORS = [
    "btech","b.tech","mtech","m.tech","mba","mca","bca","bba",
    "cse","it","aiml","ai ml","ece","civil","mechanical","ds","ece","cy","ai",
    "syllabus","seats","duration","fees","eligibility","placement",
    "jee main","admission process","counselling","autonomous","document","wifi",
    "non veg","washing machine","club","niet"
]
FULL_FORM_COURSES = [
    # UG / PG full course names
    "bachelor of computer applications",
    "bachelor of business administration",
    "master of computer applications",
    "master of business administration",

    # B.Tech / M.Tech generic
    "bachelor of technology",
    "master of technology",

    # B.Tech branches (full form)
    "bachelor of technology in computer science",
    "bachelor of technology in computer science engineering",
    "bachelor of technology in electronics",
    "bachelor of technology in electronics and communication",
    "bachelor of technology in electronics and communication engineering",
    "bachelor of technology in mechanical engineering",
    "bachelor of technology in information technology",
    "bachelor of technology in biotechnology",
    "bachelor of technology in civil engineering",
    "bachelor of technology in artificial intelligence",
    "bachelor of technology in data science",

    # Common spoken variants
    "computer science engineering",
    "electronics and communication engineering",
    "mechanical engineering",
    "information technology engineering",
    "biotechnology engineering",
]


@app.post("/chat")
def chat(req: QueryRequest):
    user_query = req.question.strip()
    lowered = user_query.lower()

    is_course_query = (
    any(word in lowered for word in COURSE_INDICATORS)
    or any(full in lowered for full in FULL_FORM_COURSES)
)
    if lowered in GREETINGS:
        return {"source":"llm-greeting","answer": ask_ollama_with_context(lowered)}
    if not is_course_query:
        return {
            "source": "chat-mode",
            "answer": "Thank you! 😄 I'm here to help. Tell me which course or topic you want information about!"
        }
    if any(g in lowered for g in SMALL_TALK):
        return {
            "source": "llm-smalltalk",
            "answer": "I'm doing great! 😄 How are you? How can I help you today?"
        }
    if not any(word in lowered for word in COURSE_INDICATORS):
        return {
        "source": "chat-mode",
        "answer": "Thank you! 😄 I'm here to help. Tell me which course or topic you want information about!"
    }
    for g in GREETINGS:
        if lowered.startswith(g + " "):
            return {"source":"llm-greeting-question","answer": ask_ollama_with_context(lowered)}

    rag_answer = answer_rag(lowered)
    if rag_answer:
        if isinstance(rag_answer, dict):
            return rag_answer
        return {"source":"rag","answer": rag_answer}

    return {"source":"none","answer":"I don't have data for this. Please re-check your question."}
