from sqlalchemy.orm import Session

from app.services.semantic_search import semantic_search
from app.services.llm_service import generate_answer


def generate_rag_answer(
    db: Session,
    question: str,
    limit: int = 5
):
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    # Step 1: Find relevant knowledge-base chunks
    results = semantic_search(
        db=db,
        query=question,
        limit=limit
    )

    # Step 2: Handle no results
    if not results:
        return {
            "answer": (
                "I could not find relevant information in the "
                "OpsMind knowledge base to answer this question."
            ),
            "sources": []
        }

    # Step 3: Build context for the LLM
    context_parts = []
    sources = []

    for chunk, distance in results:
        context_parts.append(
            f"""
Knowledge Base Chunk:
{chunk.content}
"""
        )

        sources.append({
            "chunk_id": chunk.id,
            "document_id": chunk.document_id,
            "chunk_index": chunk.chunk_index,
            "distance": float(distance)
        })

    context = "\n".join(context_parts)

    # Step 4: Ask Groq using retrieved context
    answer = generate_answer(
        question=question,
        context=context
    )

    # Step 5: Return answer + evidence sources
    return {
        "answer": answer,
        "sources": sources
    }