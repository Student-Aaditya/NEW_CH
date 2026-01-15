import os, json, uuid, re

RAW_INPUT = "RAG/Json_Format_Data/admission.json"
OUTPUT_DIR = "RAG/data"
OUTPUT_FILE = f"{OUTPUT_DIR}/admission_chunks.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_name(text):
    return re.sub(r"[_-]+", " ", text).replace("Admission", "").replace("First Year", "First Year ").strip()

def make_chunk(course_key, question, answer):
    keywords = list(set(question.lower().split()[:5] + course_key.lower().split("_")[:3]))
    return {
        "id": f"admission_{uuid.uuid4().hex[:6]}",
        "category": "admission",
        "course": course_key,
        "question": question,
        "answer": answer,
        "keywords": keywords
    }

def convert_admission():
    with open(RAW_INPUT, "r", encoding="utf-8") as f:
        raw = json.load(f)

    chunks = []

    for main_cat, subcats in raw["Admission_through"].items():

        # ---------------------- COUNSELLING ROUTE ----------------------
        if isinstance(subcats, dict):
            for course_section, rules in subcats.items():
                course_name = clean_name(course_section)
                question = f"What is the admission process for {course_name}?"
                answer = " ".join(rules)
                chunks.append(make_chunk(course_name, question, answer))

        # ---------------------- TWINNING / SPECIAL ROUTES ----------------------
        if isinstance(subcats, list):
            question = "What is the Twinning admission process?"
            answer = " ".join(subcats)
            chunks.append(make_chunk("twinning_program", question, answer))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4, ensure_ascii=False)

    print("🎉 Admission chunks created successfully!")
    print(f"📁 Saved to: {OUTPUT_FILE}")
    print(f"📦 Total Chunks: {len(chunks)}")

if __name__ == "__main__":
    convert_admission()
