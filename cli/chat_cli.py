# cli/chat_cli.py

import requests

API_URL = "http://127.0.0.1:8000/api/ask"


def main():
    print("🎬 Agentic Movie Graph CLI")
    print("Type 'exit' or 'quit' to leave.\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            print("Bye!")
            break

        payload = {
            "question": question,
            "top_k": 5,
            "debug": False,
            "return_context": False,
        }

        try:
            resp = requests.post(API_URL, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            print(f"Agent: {data.get('answer')}\n")
        except Exception as e:
            print(f"[ERROR] Request failed: {e}\n")


if __name__ == "__main__":
    main()
