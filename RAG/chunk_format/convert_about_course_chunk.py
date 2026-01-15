import os, json, uuid

RAW_INPUT = "RAG/Json_Format_Data/about_courses.json"
OUTPUT_DIR = "RAG/data"
OUTPUT_FILE = f"{OUTPUT_DIR}/about_course_chunks.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_about_chunk(key, name, summary):
    keywords = list(set(name.lower().split()[:4] + summary.lower().split()[:4]))
    return {
        "id": f"course_about_{uuid.uuid4().hex[:6]}_{key}",
        "category": "course_about",
        "question": f"Tell me about {name}.",
        "answer": summary,
        "keywords": keywords
    }

def convert_about_courses():
    with open(RAW_INPUT, "r", encoding="utf-8") as f:
        raw = json.load(f)

    chunks = []
    for key, data in raw.items():
        name = key.replace("-", " ").replace("b tech", "B Tech").title()
        summary = data.get("summary", "").strip()

        if summary:
            chunks.append(create_about_chunk(key, name, summary))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(chunks, out, indent=4, ensure_ascii=False)

    print("🎉 About Course chunks created successfully!")
    print(f"📁 Saved to: {OUTPUT_FILE}")
    print(f"📦 Total Chunks: {len(chunks)}")

if __name__ == "__main__":
    convert_about_courses()
