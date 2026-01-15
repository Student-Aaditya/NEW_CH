import os, json, uuid

RAW_DIR = "RAG/Json_Format_Data"
OUTPUT_DIR = "RAG/data"
OUTPUT_FILE = f"{OUTPUT_DIR}/combined_chunks.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)
chunks = []

def make_chunk(category, question, answer):
    keywords = list(set(question.lower().split()[:5] + answer.lower().split()[:5]))
    return {
        "id": f"{category}_{uuid.uuid4().hex[:6]}",
        "category": category,
        "question": question.strip(),
        "answer": answer.strip(),
        "keywords": keywords
    }

# ------------------ 1️⃣ FAQ Data ------------------
faq_path = os.path.join(RAW_DIR, "faq_data.json")
if os.path.exists(faq_path):
    data = json.load(open(faq_path, "r", encoding="utf-8"))
    for row in data:
        q = row.get("question", [""])[0]
        a = row.get("answer", [""])[0]
        if q and a:
            chunks.append(make_chunk("faq", q, a))

# ------------------ 2️⃣ Hostel & Facilities ------------------
hostel_path = os.path.join(RAW_DIR, "hostel_facilities.json")
if os.path.exists(hostel_path):
    data = json.load(open(hostel_path, "r", encoding="utf-8"))
    for item in data:
        text = item.get("text", "")
        topic = item.get("topic", "")
        if text:
            question = f"What about {topic.replace('_',' ')} in hostel?"
            chunks.append(make_chunk("hostel_facility", question, text))

# ------------------ 3️⃣ Institute Overview / Research ------------------
overview_path = os.path.join(RAW_DIR, "overview_data.json")
if os.path.exists(overview_path):
    data = json.load(open(overview_path, "r", encoding="utf-8"))

    # Overview general points
    for point in data["institute"]["overview"]:
        chunks.append(make_chunk("institute_overview", "Tell me about NIET.", point))

    # Rankings
    for rank in data["institute"]["rankings"]:
        chunks.append(make_chunk("rankings", "What are NIET rankings?", rank))

    # Awards
    for award in data["institute"]["awards"]:
        chunks.append(make_chunk("awards", "What awards has NIET received?", award))

    # Research overview
    for research in data["research"]["overview"]:
        chunks.append(make_chunk("research_info", "Explain NIET research focus.", research))

    # Research areas
    for area in data["research"]["areas"]:
        chunks.append(make_chunk("research_area", f"Research area at NIET?", area))

    # Facilities
    for fac in data["facilities"]:
        chunks.append(make_chunk("facilities", "What facilities does NIET have?", fac))

# ------------------ SAVE FINAL CHUNK FILE ------------------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=4, ensure_ascii=False)

print("🎉 Combined chunks created successfully!")
print(f"📁 Saved: {OUTPUT_FILE}")
print(f"📦 Total Chunks: {len(chunks)}")
