import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from query_rag import answer_from_rag

test_queries = [
#     "What is Kathputliyaan club?",
#     "Non veg in hostel?",
#     "Tell me about BTech CSE",
#     "What is NIET?",
    # "Admission process for Twiining Porgram",
    # "placement record of cse?",
    # "washing machine facilities"
#     "btech cse syllabus pdf?",
#     "Indoor sports clubs?",
    # "Tell me full details about B.Tech CSE  in NIET",
    # "tell me about cse aiml",
    # "list of clubs available in niet",
    # "List Of Different Type Of Cultural And Hooby",
    # "Nritya Bhakti (Traditional Dance ) Club",
    # "Table Tenn Club"
    "syllabus for btech cse it twinning",
        "syllabus for mtech cse ai",
    
]

print("🔍 RAG Test Suite Running...\n")

for q in test_queries:
    print(f"❓ Query: {q}")
    print(answer_from_rag(q))
    print("-" * 60)
