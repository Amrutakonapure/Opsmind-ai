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


def generate_incident_analysis(
    incident_title: str,
    incident_description: str,
    incident_severity: str,
    service_name: str,
    logs: str,
    context: str
) -> str:

    prompt = f"""
You are OpsMind AI, an expert IT incident root-cause analysis assistant.

Analyze the following production incident using the incident details,
logs, and retrieved knowledge-base context.

INCIDENT
--------
Title: {incident_title}
Description: {incident_description}
Current Severity: {incident_severity}
Service: {service_name}

LOGS
----
{logs}

KNOWLEDGE BASE
--------------
{context}

Return your response ONLY as valid JSON using exactly this structure:

{{
    "severity": "LOW|MEDIUM|HIGH|CRITICAL",
    "probable_cause": "Most likely root cause based on the evidence.",
    "recommendations": "Practical steps an engineer should take.",
    "confidence": 0.0
}}

Rules:
1. Use the knowledge base and incident evidence as your primary sources.
2. Do not invent facts.
3. The severity must be one of LOW, MEDIUM, HIGH, or CRITICAL.
4. Confidence must be a number between 0.0 and 1.0.
5. If evidence is insufficient, lower the confidence.
6. Clearly state uncertainty when appropriate.
7. Return ONLY JSON.
"""

    response = client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {
                "role": "system",
                "content": "You are a reliable IT root-cause analysis assistant. Return only valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    return response.choices[0].message.content