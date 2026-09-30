from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embedding(text: str) -> list[float]:
    """
    Generate a 384-dimensional embedding for a text.
    """

    if not text or not text.strip():
        raise ValueError("Cannot generate embedding for empty text.")

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()