import os, json, uuid

RAW_INPUT = "RAG/Json_Format_Data/placement_chunks.json"   # your provided file
OUTPUT_DIR = "RAG/data"
OUTPUT_FILE = f"{OUTPUT_DIR}/placements_final_chunks.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def make_chunk(dept, question, answer):
    keywords = list(set(dept.lower().split() + question.lower().split()[:4]))
    return {
        "id": f"placement_{uuid.uuid4().hex[:6]}",
        "category": "placement",
        "question": question.strip(),
        "answer": answer.strip(),
        "keywords": keywords
    }

def convert_placement_chunks():
    with open(RAW_INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = []

    for item in data:
        dept = item.get("department", "").strip()
        metric = item.get("metric", "").strip()
        value = item.get("value", "").strip()
        url = item.get("url", "").strip()
        text = item.get("text", "").strip()

        dept_clean = dept.replace("And", "&").title()

        # Q/A Generation by metric type
        if metric == "placements_offered":
            chunks.append(make_chunk(
                dept_clean,
                f"How many placements in {dept_clean}?",
                f"{dept_clean} recorded {value} placements. More info: {url}"
            ))

        elif metric == "highest_package":
            chunks.append(make_chunk(
                dept_clean,
                f"What is the highest package in {dept_clean}?",
                f"The highest package in {dept_clean} is {value}. More info: {url}"
            ))

        elif metric == "average_package":
            chunks.append(make_chunk(
                dept_clean,
                f"What is the average package in {dept_clean}?",
                f"The average package in {dept_clean} is {value}. More info: {url}"
            ))

        # Generic overview for each dept
        if text:
            chunks.append(make_chunk(
                dept_clean,
                f"Tell me about placements in {dept_clean}.",
                text
            ))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(chunks, out, indent=4, ensure_ascii=False)

    print("🎉 Placement chunks created successfully!")
    print(f"📁 Saved to: {OUTPUT_FILE}")
    print(f"📦 Total Chunks: {len(chunks)}")

if __name__ == "__main__":
    convert_placement_chunks()
