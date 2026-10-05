from groq import Groq

from app.core.database import settings


client = Groq(
    api_key=settings.groq_api_key
)


def generate_answer(question: str, context: str) -> str:
    prompt = f"""
You are OpsMind AI, an IT incident management assistant.

Your job is to analyze IT incidents using the provided
knowledge-base context.

Follow these rules:

1. Use the provided context as your primary source.
2. Do not invent facts that are not supported by the context.
3. If the context is insufficient, clearly say so.
4. Identify the most likely root cause when possible.
5. Explain the evidence supporting your conclusion.
6. Provide practical troubleshooting recommendations.
7. Do not claim certainty when the evidence is weak.
8. Keep the answer clear and useful for an IT engineer.

Knowledge-base context:
-----------------------
{context}
-----------------------

User question:
{question}
"""

    response = client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {
                "role": "system",
                "content": "You are a reliable IT operations assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content