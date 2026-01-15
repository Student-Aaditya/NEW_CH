import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # go to project root

from Ollama.llm_client import ask_ollama_with_context
from RAG.router.syllabus_router import syllabus_router
# ================================================
# CONFIG & PATH SETUP
# ================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAISS_PATH = os.path.join(BASE_DIR, "vector_store.faiss")
VEC_PATH = os.path.join(BASE_DIR, "vectors.npy")
META_PATH = os.path.join(BASE_DIR, "metadata_cleaned.json")


# Load Model
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

# Load Vector Store
index = faiss.read_index(FAISS_PATH)
metadata = json.load(open(META_PATH, "r", encoding="utf-8"))
vectors = np.load(VEC_PATH)
#fuzzy matching for message mistake
from difflib import SequenceMatcher

def fuzzy_match(user, target):
    return SequenceMatcher(None, user, target).ratio() >= 0.55
#reading metadata json 
with open(META_PATH, "r", encoding="utf-8") as f:
    METADATA = json.load(f)

#normalize for clean and matching data
def normalize_query(q: str):
    q = q.lower()
    corrections = {
        "twiining": "twinning",
        "twining": "twinning",
        "porgram": "program",
        "btech": "b.tech",
        "cs": "cse",
        "ai ml": "aiml",
        "ml": "aiml",
        "addmission": "admission",
        "admsision": "admission"
    }
    for wrong, right in corrections.items():
        q = q.replace(wrong, right)
    return q.strip()

def detect_intent(q: str):
    q = normalize_query(q)
    intents = {
        "twinning": ["twinning","international twinning","exchange program"],
        "admission": ["admission","apply","eligibility","counselling","direct admission"],
        "placement": ["placement","package","average package","highest package"],
        "hostel": ["hostel","wifi","food","laundry","rooms","non veg"],
        "club": ["club","music club","dance club","drama","sports club"],
        "cultural_hobby": ["cultural","hobby","cultural club","hobby club","extracurricular","activities","festival","art","traditional"],
        "hostel": ["hostel","mess","wifi","food","laundry","tea","canteen",
        "non veg","non-veg","veg","room","ac room","hot water"],
        "scholarship":["scholar ship","scholar-ship","scheme"],
        "bus":["bus facilities","transport facilities","transport"],
        "syllabus": [
        "syllabus","subject list","subjects","semester wise",
        "course structure","download syllabus",
        "btech aiml","aiml syllabus","cse aiml","btech cse aiml"],
        "aiml":["btech aiml","btech cse aiml","ai ml"],
        "it":["btech it","btech information technology"]
        
}
    for key, words in intents.items():
        for w in words:
            if w in q:
                return key
    return None

#club detect intent 
def club_lookup(q):
    q = normalize_query(q)
    for item in METADATA:
        if "club" in item.get("question","").lower():
            if fuzzy_match(q, item["question"].lower()):
                return item["answer"]
    return None

#for twinning program 
def twinning_router(q):
    q = normalize_query(q)
    for item in METADATA:
        if "twinning" in item.get("question","").lower():
            if "admission" in q or "process" in q or "eligibility" in q:
                return item["answer"]
    return None

#for admission intent
def handle_admission(q):
    q = normalize_query(q)
    for item in METADATA:
        if "admission" in item["question"].lower():
            return item["answer"]
    return None

#for placement intent

with open("RAG/Json_Format_Data/placement_chunks.json","r",encoding="utf-8") as f:
    PLACEMENT_DATA = json.load(f)

DEPT_ALIASES = {
    "cs": ["cs","computer science"],
    "csbs": ["csbs","computer science and business system"],
    "ai": ["ai","artificial intelligence"],
    "iot": ["iot","internet of things","btech iot"],
    "ece": ["ece","electronics","communication"],
    "me": ["mechanical"],
    "biotech": ["biotech","biotechnology"],
    "mca": ["mca","master of computer application"],
    "mba": ["mba","master of business administration"],
    "cse": [
        "cse","c s e","computer science","computer science engineering",
        "btech cse","b tech cse","cse eng","cse engineering","btech cse a"
    ],
    "aiml": [
        "aiml","ai ml","artificial intelligence","machine learning",
        "artificial intelligence machine language","btech aiml","cse aiml",
        "btech cse aiml","cse a","btech cse a"
    ],
    "ds": [
        "ds","data science","btech ds","cse ds","btech data science"
    ]
}

METRIC_MAP = {
    "highest": "highest_package",
    "top": "highest_package",
    "max": "highest_package",
    "average": "average_package",
    "avg": "average_package",
    "salary": "highest_package",
    "package": "highest_package",
    "placements": "placements_offered",
    "placed": "placements_offered",
    "placement":"placement_offere"
}

import json

with open("RAG/data/admission_chunks.json","r",encoding="utf-8") as f:
    ADMISSION_DATA = json.load(f)

ADMISSION_KEYWORDS = {
    "jee": ["jee", "jee main", "uptu", "uptu counselling"],
    "direct": ["direct", "direct admission", "without jee"],
    "management": ["management quota", "management seat"],
    "twinning": ["twinning", "international program", "study abroad"],
    "lateral": ["lateral entry", "2nd year admission", "diploma to btech"],
    "btech": ["btech", "engineering"],
    "mca": ["mca"],
    "mba": ["mba"],
    "pgdm": ["pgdm"],
    "bpharm": ["bpharm" , "b.pharm"],
    "mtech": ["mtech", "m.tech"]
}


def admission_router(query: str):
    q = query.lower()

    if not any(k in q for k in ["admission","apply","eligibility","jee","direct","quota","process"]):
        return None
    
    for key, aliases in ADMISSION_KEYWORDS.items():
        if any(a in q for a in aliases):
            for item in ADMISSION_DATA:
                if key in item["course"].lower() or key in item["question"].lower():
                    return f"Admission – {item['course']}**\n{item['answer']}"

    if "jee" in q or "jee main" in q:
        return "Yes, you CAN get admission through JEE Main counselling as per AKTU/UPTAC process. For more information visit https://www.niet.co.in/admissions/eligibility-admission-process"

    if "direct admission" in q or "direct" in q:
        return "Yes, direct admission is possible under management quota as per UP/AKTU guidelines. For more information visit https://www.niet.co.in/admissions/direct-admission"

    for item in ADMISSION_DATA:
        if "admission process" in item["question"].lower():
            return item["answer"]

    return "Please specify: JEE Main / Direct Admission / Twinning / Lateral Entry / MCA / MBA etc."

def normalize(text: str):
    return (
        text.lower()
        .replace("b.tech","")
        .replace("btech","")
        .replace("&","and")
        .replace("(","")
        .replace(")","")
        .replace("/"," ")
        .replace("-"," ")
        .strip()
    )

def placement_router(query: str):
    q = normalize(query)

    # detect metric
    metric = None
    for k, v in METRIC_MAP.items():
        if k in q:
            metric = v
            break
    if not metric:
        metric = "average_package" if "average" in q or "avg" in q else "highest_package"

    # detect dept (with improved fuzzy match)
    matched_dept = None
    for dept, aliases in DEPT_ALIASES.items():
        for a in aliases:
            if normalize(a) in q or q in normalize(a):
                matched_dept = dept
                break
        if matched_dept:
            break

    if matched_dept is None:
        return "Please specify department like: CSE, AIML, DS, IoT, CSBS, MCA, MBA etc."


    # ======== METADATA FIRST (Primary Source) ========
    for item in METADATA:
        text_q = normalize(item.get("question",""))
        if "placement" in text_q and matched_dept in text_q:
            ans = item.get("answer","").strip()
            bullets = "• " + ans.replace(". ", ".\n• ")
            return f"""
{matched_dept.upper()} Placement Details**
{bullets}
""".strip()


    # ======== CHUNK FALLBACK ========
    for item in PLACEMENT_DATA:
        dept_name = normalize(item.get("department",""))
        if matched_dept in dept_name:
            return f"""
{item['department']} Placement Overview**
{item['value']} ({metric.replace('_',' ')})
{item['url']}
""".strip()

    return "No placement record found."


#for seat and duration 
def get_seat_duration_from_metadata(query):
    q = normalize(query)

    for item in METADATA:
        answer = normalize(item.get("answer",""))
        if any(word in answer for word in q.split()):
            
            seats = None
            duration = None

            # find seats
            if "seat" in answer:
                for token in answer.split():
                    if token.isdigit():
                        seats = token
                        break

            # find duration
            if "year" in answer:
                for token in answer.split():
                    if "year" in token:
                        duration = token
                        break

            return {
                "context": item.get("answer",""),
                "seats": seats,
                "duration": duration
            }

    return None

def seat_duration_router(query):
    info = get_seat_duration_from_metadata(query)
    if info:
        from Ollama.llm_client import ask_ollama_with_context
        return ask_ollama_with_context(query, info["context"])
    return None


#why choose 
def why_choose_router(query: str):
    q = query.lower()

    WHY_KEYS = ["why choose", "advantages", "benefits", "is good", "good for", "scope of"]

    if not any(k in q for k in WHY_KEYS):
        return None

    if "niet" in q:
        for item in METADATA:
            text_q = item.get("question","").lower()
            if (
                any(k in text_q for k in WHY_KEYS) or
                "tell me about" in text_q or
                "about" in text_q or
                "course_about" in item.get("category","").lower()
            ):
                text = item.get("answer","").strip()
                bullets = "• " + text.replace(". ", ".\n• ")
                return f"""
Why Choose {item['question'].replace('Tell me about','').strip()} at NIET?

{bullets}
""".strip()

    return ask_ollama_with_context(
        query,
        "Respond only in bullet points, course scope, skills gained, duration, and career opportunities. Do NOT mention NIET unless the query contains NIET."
    )


#for taking data from metadata 
def metadata_lookup(query):
    q = query.lower()
    KEYWORDS = [
        "study table","non veg","wifi","scholarship","transport","timing",
        "tea","laundry","geyser","parking","canteen","mess menu","water purifier",
        "green gold society","tennis club","editorial club","yoga club",
        "syllabus",
        #aiml and ai
        "btech aiml","aiml","cse aiml","btech cse aiml",
        "btech cse ai","cse ai"

        #data science
        "data science","cse data science","btech data science"

        #cyber security
        "cyber security","cy","cyber-security","btech cse cy","btech cse cyber security"

        #iot
        "information technology","btech iot","btech cse iot","btech cse information technology"

    ]

    for item in METADATA:
        question = item.get("question","").lower()

        if any(key in q for key in KEYWORDS):
            if any(key in question for key in q.split()):
                return item.get("answer")
    return None



def rag_search(query, top_k=5, threshold=0.25):
    texts = [f"{item['question']} {item['answer']}" for item in metadata]
    q_vec = model.encode([query]).astype("float32")
    distances, indices = index.search(q_vec, top_k)

    best_score = 1 - distances[0][0]
    best_idx = indices[0][0]

    if best_score >= threshold:
        return {
            "source": "RAG",
            "confidence": float(best_score),
            "data": metadata[best_idx]
        }

    return {"source": "LLM", "confidence": float(best_score), "data": None}

#for club data
def extract_club_name(q_text: str):
    q_text = q_text.replace("What is", "").replace("what is","")
    q_text = q_text.replace("?", "").replace("club","").replace("Club","")
    return q_text.strip().title()
 
def answer_from_rag(query: str):
    query = normalize_query(query)
    intent = detect_intent(query)


    if (
    "list of clubs" in query or 
    "clubs available" in query or 
    "club list" in query or 
    "how many club" in query or 
    "different club" in query
):
        clubs = [
            c for c in METADATA
            if "club" in c["question"].lower()
            and not any(stop in c["question"].lower() for stop in [
                "how many", "list of", "different type", "outdoor", "indoor", "cultural", "hobby","list of clubs"
            ])
        ]

        formatted = "\n".join(
            f"• {extract_club_name(c['question'])}"
            for c in clubs
        )
    
        total = len(clubs)

        return (
            f"NIET currently has {total} active clubs:\n\n"
            f"{formatted}\n\n"
            f"🔗 Full list: https://niet.co.in/students-life/student-clubs-societies"
        )
    # seats and duration
    # 1️⃣ Seats & Duration Query
    sd = seat_duration_router(query)
    if sd:
        return sd

    # For Academic Syllabus 
    if  "syllabus"in query or "pdf" in query:
        syllabus=syllabus_router(query)
        return syllabus
    

    # Why Choose Router
    wc = why_choose_router(query)
    if wc:
        return wc

    #for placement
    if "placement" in query or "package" in query or "salary" in query:
        place = placement_router(query)
        if place:
            return place
    
    if intent == "hostel":

    # Non-veg availability
        if "non veg" in query or "non-veg" in query:
            return "No, non-veg is not available occasionally in the hostel mess, depending on the weekly menu & schedule."

    # Tea in mess
        if "tea" in query:
            return "Yes, tea is served in the hostel mess during breakfast & evening break."

    # Wifi
        if "wifi" in query:
            return "Yes, hostel buildings have Wi-Fi access for students."

    # Laundry
        if "laundry" in query or "washing" in query or "washing machine" in query:
            return " Yes, hostel has laundry / washing facilities."

    # If only 'mess' asked
        if "mess" in query or "food" in query:
            return "The hostel mess provides vegetarian & occasional and no non-veg meals available, with scheduled timings."

    # fallback hostel answer
        return " NIET hostel provides in-campus accommodation with canteen, mess, medical facilities, Wi-Fi, laundry & general amenities. For more infomation reach out website:- https://www.niet.co.in/campus-facilities/other-facility"

    if intent == "club":
        ans = club_lookup(query)
        if ans: return ans

        club_context = "\n".join(
            item['answer'] for item in METADATA 
            if "club" in item["question"].lower()
        )
        return ask_ollama_with_context(query, club_context)

    if intent == "cultural_hobby":
        if "list" in query or "different type" in query or "types of" in query:
            clubs = [c for c in METADATA if "club" in c["question"].lower()]
            formatted = "\n".join(
                f"• {c['question'].replace('What is', '').replace('?', '').strip()}"
                for c in clubs
            )
            return f"Here are cultural & hobby-related clubs at NIET:\n\n{formatted}\n\nFor full list: https://niet.co.in/students-life/student-clubs-societies"

        culture_context = "\n".join(
            item['answer'] for item in METADATA
            if "club" in item["question"].lower() or "cultural" in item["question"].lower()
        )
        return ask_ollama_with_context(query, culture_context)

    # Admission Router
    admission = admission_router(query)
    if admission:
        return admission 

    if intent == "hostel":
        for item in METADATA:
            if "hostel" in item["question"].lower():
                return item["answer"]

    rag_result = rag_search(query)
    if rag_result["source"] == "RAG" and rag_result["data"]:
        return rag_result["data"]["answer"]
    
    meta_hit = metadata_lookup(query)
    if meta_hit:
        return meta_hit

    return ask_ollama_with_context(query, rag_result["data"] if rag_result["data"] else "")

if __name__ == "__main__":
    while True:
        ques = input("Ask: ")
        print(answer_from_rag(ques))
