# tests/test_api.py

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health():
    """L'API doit répondre OK sur /health."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_s1_nolan_scifi():
    """
    S1 – 'Give me a sci-fi movie directed by Christopher Nolan.'
    On s'attend à voir au moins Inception ou Interstellar.
    """
    payload = {
        "question": "Give me a sci-fi movie directed by Christopher Nolan.",
        "top_k": 3,
        "debug": False,
        "return_context": False,
    }
    resp = client.post("/api/ask", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    answer = data.get("answer", "")
    answer_lower = answer.lower()

    assert answer  # non vide
    assert ("inception" in answer_lower) or ("interstellar" in answer_lower)
    # On ne force pas la présence du mot 'nolan' dans la phrase,
    # il suffit que le film proposé soit correct.



def test_s2_dicaprio_movies():
    """
    S2 – 'List movies with Leonardo DiCaprio in the graph.'
    On s'attend à voir au moins un film avec DiCaprio (Inception, etc.).
    """
    payload = {
        "question": "List movies with Leonardo DiCaprio in the graph.",
        "top_k": 5,
        "debug": False,
        "return_context": False,
    }
    resp = client.post("/api/ask", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    answer = data.get("answer", "")
    answer_lower = answer.lower()

    assert answer
    assert "leonardo" in answer_lower  # mention de l'acteur
    # au moins un des titres de ton mini graphe
    assert ("inception" in answer_lower) or ("dark knight" in answer_lower)


def test_s3_sci_fi_and_director():
    """
    S3 – 'Which movies in the graph are sci-fi and who directed them?'
    On veut que la réponse cite un film sci-fi + Christopher Nolan.
    """
    payload = {
        "question": "Which movies in the graph are sci-fi and who directed them?",
        "top_k": 5,
        "debug": False,
        "return_context": False,
    }
    resp = client.post("/api/ask", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    answer = data.get("answer", "")
    answer_lower = answer.lower()

    assert answer
    # un titre sci-fi
    assert ("inception" in answer_lower) or ("interstellar" in answer_lower)
    # mention du réalisateur
    assert "nolan" in answer_lower
