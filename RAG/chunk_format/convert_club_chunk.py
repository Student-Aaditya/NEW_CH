import os, json, uuid

RAW_INPUT = "RAG/Json_Format_Data/club_data.json"  # your provided file
OUTPUT_DIR = "RAG/data"
OUTPUT_FILE = f"{OUTPUT_DIR}/club_chunks.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def normalize_club_name(text):
    """Clean club names from question formats like 'What/Tell about...'."""
    text = text.replace("What", "").replace("Tell", "").replace("about", "").replace("is", "")
    text = text.replace("Club", "").replace("club", "")
    return text.strip(" ?").title()


def create_club_chunk(club_name, question, answer):
    base_keywords = club_name.lower().replace("&", " ").split()[:3]
    q_words = question.lower().split()[:3]
    a_words = answer.lower().split()[:3]

    keywords = list(set(base_keywords + q_words + a_words))

    return {
        "id": f"club_{uuid.uuid4().hex[:6]}",
        "category": "club",
        "club_name": club_name,
        "question": question.strip(),
        "answer": answer.strip(),
        "keywords": keywords
    }


def convert_clubs():
    with open(RAW_INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = []

    for item in data:
        questions = item.get("question", [])
        answers = item.get("answer", [])

        if not questions or not answers:
            continue

        # handle multiple questions & answers per item
        for q in questions:
            club_name = normalize_club_name(q)
            for a in answers:
                chunks.append(create_club_chunk(
                    club_name,
                    f"What is {club_name} Club?",
                    a
                ))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(chunks, out, indent=4, ensure_ascii=False)

    print("🎉 Club chunks created successfully!")
    print(f"📁 Saved to: {OUTPUT_FILE}")
    print(f"📦 Total Chunks: {len(chunks)}")


if __name__ == "__main__":
    convert_clubs()
