from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import generate_embedding


def main():
    db = SessionLocal()

    try:
        query = "The payment service is responding very slowly."

        query_embedding = generate_embedding(query)

        results = (
            db.query(DocumentChunk)
            .filter(DocumentChunk.embedding.is_not(None))
            .order_by(
                DocumentChunk.embedding.cosine_distance(
                    query_embedding
                )
            )
            .limit(5)
            .all()
        )

        print("\nQuery:")
        print(query)

        print("\nMost similar chunks:\n")

        for index, chunk in enumerate(results, start=1):
            print(f"{index}.")
            print(chunk.content[:300])
            print("-" * 60)

    finally:
        db.close()


if __name__ == "__main__":
    main()