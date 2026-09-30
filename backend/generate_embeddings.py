from app.core.database import SessionLocal
from app.services.embedding_pipeline import (
    generate_embeddings_for_chunks
)


def main():
    db = SessionLocal()

    try:
        processed = generate_embeddings_for_chunks(db)

        print(
            f"Generated embeddings for {processed} chunks."
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()