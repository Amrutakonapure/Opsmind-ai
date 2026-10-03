from app.core.database import SessionLocal
from app.services.semantic_search import semantic_search


def main():
    db = SessionLocal()

    try:
        query = "Payment service is responding very slowly"

        results = semantic_search(
            db=db,
            query=query,
            limit=5
        )

        print("\nQuery:")
        print(query)

        print("\nTop results:\n")

        for index, (chunk, distance) in enumerate(
            results,
            start=1
        ):
            print(f"Result {index}")
            print(f"Chunk ID: {chunk.id}")
            print(f"Document ID: {chunk.document_id}")
            print(f"Distance: {float(distance):.4f}")
            print(f"Content: {chunk.content[:300]}")
            print("-" * 70)

    finally:
        db.close()


if __name__ == "__main__":
    main()