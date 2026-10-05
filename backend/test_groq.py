from app.services.llm_service import generate_answer


context = """
Payment API experienced high latency during peak traffic.
Historical incidents show that database connection pool
exhaustion can cause increased API response times.
Increasing the connection pool and reducing long-running
database queries resolved similar incidents previously.
"""

question = "What is the likely cause of the payment API latency?"

answer = generate_answer(
    question=question,
    context=context
)

print("\n===== GROQ RESPONSE =====\n")
print(answer)