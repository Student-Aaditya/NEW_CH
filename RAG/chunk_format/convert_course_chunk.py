import os, json, uuid

RAW_DIR = "RAG/Json_Format_Data"
CHUNK_DIR = "RAG/data"

os.makedirs(CHUNK_DIR, exist_ok=True)

def create_chunk(category, question, answer, course_key):
    keywords = list(set(question.lower().split()[:5] + answer.lower().split()[:5]))
    return {
        "id": f"{category}_{uuid.uuid4().hex[:6]}_{course_key}",
        "category": category,
        "question": question.strip(),
        "answer": answer.strip(),
        "keywords": keywords
    }

def process_file(filename):
    file_path = os.path.join(RAW_DIR, filename)
    with open(file_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    chunk_list = []
    for key, data in raw.items():
        name = data.get("course_name", "").strip()
        duration = data.get("duration", "Not Available").strip()
        seats = data.get("seats", "Not Available").strip()
        mode = data.get("mode", "Not Available").strip()
        why = data.get("why_choose", [])
        url = data.get("source_url", "")

        # Overview
        chunk_list.append(create_chunk(
            "course_overview",
            f"What is {name}?",
            f"{name} is a {duration} program with {seats} seats ({mode}). More info: {url}",
            key
        ))

        # Duration
        chunk_list.append(create_chunk(
            "course_duration",
            f"What is the duration of {name}?",
            f"The duration of {name} is {duration}.",
            key
        ))

        # Seats
        chunk_list.append(create_chunk(
            "course_seats",
            f"How many seats for {name}?",
            f"{name} has {seats} seats.",
            key
        ))

        # Why Choose (split into chunks)
        for point in why:
            if point.strip():
                chunk_list.append(create_chunk(
                    "course_advantages",
                    f"Why choose {name} at NIET?",
                    point,
                    key
                ))

    output_file = os.path.join(CHUNK_DIR, filename.replace(".json", "_chunks.json"))
    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(chunk_list, out, indent=4, ensure_ascii=False)

    print(f"✔ Converted: {filename} → {output_file} ({len(chunk_list)} chunks)")

def convert_all():
    for file in os.listdir(RAW_DIR):
        if file.endswith(".json"):
            process_file(file)
    print("\n🎉 All files converted! Chunk files are ready in RAG/data\n")

if __name__ == "__main__":
    convert_all()
