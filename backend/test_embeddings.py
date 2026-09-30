from app.services.embedding_service import generate_embedding


text = "Payment API is experiencing high latency."

embedding = generate_embedding(text)

print("Embedding generated successfully.")
print("Dimensions:", len(embedding))
print("First 5 values:", embedding[:5])