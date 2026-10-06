import json

from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.models.ai_analysis import AIAnalysis
from app.services.semantic_search import semantic_search
from app.services.llm_service import generate_incident_analysis


def analyze_incident(
    db: Session,
    incident_id: int
):
    # 1. Get incident
    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if not incident:
        raise ValueError("Incident not found.")

    # 2. Collect incident logs
    logs_text = ""

    if incident.logs:
        log_entries = []

        for log in incident.logs:
            log_entries.append(
                f"[{log.level}] {log.message}"
            )

        logs_text = "\n".join(log_entries)

    else:
        logs_text = "No logs available for this incident."

    # 3. Build search query
    search_query = f"""
Incident:
{incident.title}

Description:
{incident.description}

Service:
{incident.service.name}
"""

    # 4. Retrieve relevant knowledge
    search_results = semantic_search(
        db=db,
        query=search_query,
        limit=5
    )

    context_parts = []

    for chunk, distance in search_results:
        context_parts.append(
            f"""
Knowledge Base Chunk:
{chunk.content}
"""
        )

    if context_parts:
        context = "\n".join(context_parts)
    else:
        context = "No relevant knowledge-base information found."

    # 5. Ask Groq for structured analysis
    raw_response = generate_incident_analysis(
        incident_title=incident.title,
        incident_description=incident.description,
        incident_severity=incident.severity,
        service_name=incident.service.name,
        logs=logs_text,
        context=context
    )

    # 6. Parse JSON returned by LLM
    try:
        analysis_data = json.loads(raw_response)
    except json.JSONDecodeError:
        raise ValueError(
            "AI returned an invalid JSON response."
        )

    # 7. Validate required fields
    required_fields = [
        "severity",
        "probable_cause",
        "recommendations",
        "confidence"
    ]

    for field in required_fields:
        if field not in analysis_data:
            raise ValueError(
                f"AI response missing required field: {field}"
            )

    # 8. Validate severity
    allowed_severities = {
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    }

    severity = analysis_data["severity"].upper()

    if severity not in allowed_severities:
        severity = incident.severity

    # 9. Validate confidence
    confidence = float(analysis_data["confidence"])

    confidence = max(
        0.0,
        min(1.0, confidence)
    )

    # 10. Save AI analysis
    ai_analysis = AIAnalysis(
        incident_id=incident.id,
        severity=severity,
        probable_cause=str(
            analysis_data["probable_cause"]
        ),
        recommendations=str(
            analysis_data["recommendations"]
        ),
        confidence=confidence
    )

    db.add(ai_analysis)
    db.commit()
    db.refresh(ai_analysis)

    return ai_analysis