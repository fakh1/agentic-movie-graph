# test_hybrid_retrieval.py

from agents.retrieval import hybrid_retrieve

if __name__ == "__main__":
    question = "Give me a sci-fi movie directed by Christopher Nolan."
    result = hybrid_retrieve(question, top_k=3)

    print("=== CONTEXT BUILT FOR LLM ===")
    print(result["context"])
