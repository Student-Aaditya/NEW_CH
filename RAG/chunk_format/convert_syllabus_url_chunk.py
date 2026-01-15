import os, json, uuid, re

RAW_INPUT = "RAG/Json_Format_Data/url_chunks.json"
OUTPUT_DIR = "RAG/data"
OUTPUT_FILE = f"{OUTPUT_DIR}/url_final_chunks.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def normalize_course_name(name: str):
    """Format course name to proper case for user display."""
    name = name.replace("_", " ").replace("&", " ").strip()
    return name.upper() if "btech" in name or "mtech" in name else name.title()

def make_url_chunk(course, question, answer, aliases):
    keyword_base = course.lower().split()[:3] + [k.lower() for k in aliases[:3]]
    return {
        "id": f"url_{uuid.uuid4().hex[:6]}",
        "category": "syllabus_url",
        "course": course,
        "question": question,
        "answer": answer,
        "keywords": list(set(keyword_base + ["syllabus", "pdf", "download", "link"]))
    }

def convert_urls():
    with open(RAW_INPUT, "r", encoding="utf-8") as f:
        raw = json.load(f)

    chunks = []
    for item in raw:
        course = item.get("course", "").strip()
        aliases = item.get("aliases", [])
        url = item.get("syllabus_url", "").strip()

        course_name = normalize_course_name(course)

        # Case 1: There is a URL (valid syllabus link)
        if url:
            q = f"Where can I download the syllabus for {course_name}?"
            a = f"You can download the syllabus for **{course_name}** here:\n{url}"
            chunks.append(make_url_chunk(course_name, q, a, aliases))

        # Case 2: Missing URL → respond gracefully
        else:
            q = f"Is syllabus available for {course_name}?"
            a = f"No official syllabus URL was provided for {course_name}. Contact NIET Academics for updated links."
            chunks.append(make_url_chunk(course_name, q, a, aliases))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(chunks, out, indent=4, ensure_ascii=False)

    print("🎉 URL syllabus chunks created successfully!")
    print(f"📁 Saved to: {OUTPUT_FILE}")
    print(f"📦 Total chunks: {len(chunks)}")


if __name__ == "__main__":
    convert_urls()
