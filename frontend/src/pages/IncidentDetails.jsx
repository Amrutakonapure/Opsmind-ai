import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  ArrowLeft,
  Clock,
  FileText,
  Server,
  Brain,
} from "lucide-react";

import "../Dashboard.css";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import api from "../services/api";

function IncidentDetails() {
  const { id } = useParams();
  const navigate = useNavigate();

  // Incident state
  const [incident, setIncident] = useState(null);

  // Loading/error state
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // AI analysis state
  const [aiAnalysis, setAiAnalysis] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [aiError, setAiError] = useState("");

  const [timeline, setTimeline] = useState([]);
  const [timelineLoading, setTimelineLoading] = useState(true);

  // Load incident whenever incident ID changes
  useEffect(() => {
  loadIncident();
  loadTimeline();

  setAiAnalysis(null);
  setAiError("");
}, [id]);

  // --------------------------------------------------
  // LOAD INCIDENT
  // --------------------------------------------------

  const loadIncident = async () => {
    try {
      setLoading(true);
      setError("");

      const [
        incidentResponse,
        servicesResponse,
      ] = await Promise.all([
        api.get(`/incidents/${id}/details`),
        api.get("/services"),
      ]);

      const incidentData = incidentResponse.data;
      const services = servicesResponse.data;

      // Find service name using service_id
      const service = services.find(
        (service) =>
          service.id === incidentData.service_id
      );

      setIncident({
        ...incidentData,
        serviceName:
          service?.name ||
          `Service #${incidentData.service_id}`,
      });
    } catch (error) {
      console.error(
        "Failed to load incident:",
        error
      );

      const backendMessage =
        error.response?.data?.detail;

      setError(
        backendMessage ||
          "Unable to load incident details."
      );
    } finally {
      setLoading(false);
    }
  };


  const loadTimeline = async () => {
    try {
       setTimelineLoading(true);

       const response = await api.get(
        `/incidents/${id}/timeline`
       );

       setTimeline(response.data);
     } catch (error) {
       console.error(
        "Failed to load incident timeline:",
        error
       );

       setTimeline([]);
     } finally {
       setTimelineLoading(false);
     }
  };

  // --------------------------------------------------
  // AI ROOT CAUSE ANALYSIS
  // --------------------------------------------------

  const handleAnalyzeWithAI = async () => {
    try {
      setAnalyzing(true);
      setAiError("");

      const response = await api.post(
        `/ai/incidents/${id}/analyze`
      );

      setAiAnalysis(response.data);
    } catch (error) {
      console.error(
        "AI analysis failed:",
        error
      );

      const backendMessage =
        error.response?.data?.detail;

      setAiError(
        backendMessage ||
          "Unable to analyze this incident."
      );
    } finally {
      setAnalyzing(false);
    }
  };

  // --------------------------------------------------
  // LOADING SCREEN
  // --------------------------------------------------

  if (loading) {
    return (
      <div className="dashboard-layout">
        <Sidebar />

        <main className="dashboard-main">
          <Navbar />

          <section className="dashboard-content">
            <p>
              Loading incident...
            </p>
          </section>
        </main>
      </div>
    );
  }

  // --------------------------------------------------
  // ERROR SCREEN
  // --------------------------------------------------

  if (error || !incident) {
    return (
      <div className="dashboard-layout">
        <Sidebar />

        <main className="dashboard-main">
          <Navbar />

          <section className="dashboard-content">
            <p>
              {error ||
                "Incident not found."}
            </p>

            <button
              className="back-button"
              onClick={() =>
                navigate("/incidents")
              }
            >
              <ArrowLeft size={18} />
              Back to Incidents
            </button>
          </section>
        </main>
      </div>
    );
  }

  // --------------------------------------------------
  // MAIN PAGE
  // --------------------------------------------------

  return (
    <div className="dashboard-layout">
      <Sidebar />

      <main className="dashboard-main">
        <Navbar />

        <section className="dashboard-content">

          {/* ==========================================
              BACK BUTTON
          ========================================== */}

          <button
            className="back-button"
            onClick={() =>
              navigate("/incidents")
            }
          >
            <ArrowLeft size={18} />
            Back to Incidents
          </button>


          {/* ==========================================
              INCIDENT HEADER
          ========================================== */}

          <div className="incident-detail-header">

            <div>

              <div className="incident-detail-title-row">

                <h2>
                  {incident.title}
                </h2>

                <span
                  className={`severity-badge ${incident.severity.toLowerCase()}`}
                >
                  {incident.severity}
                </span>

              </div>

              <p>
                Incident #{incident.id}
              </p>

            </div>


            <span className="status-badge">
              {incident.status}
            </span>

          </div>


          {/* ==========================================
              AI ANALYSIS BUTTON
          ========================================== */}

          <div className="ai-analysis-action">

            <button
              className="analyze-ai-button"
              onClick={
                handleAnalyzeWithAI
              }
              disabled={analyzing}
            >

              <Brain size={18} />

              {analyzing
                ? "AI is analyzing..."
                : "Analyze with AI"}

            </button>

          </div>


          {/* ==========================================
              AI ERROR
          ========================================== */}

          {aiError && (
            <div className="ai-error">
              {aiError}
            </div>
          )}


          {/* ==========================================
              AI ANALYSIS RESULT
          ========================================== */}

          {aiAnalysis && (

            <section className="ai-analysis-card">

              <div className="ai-analysis-header">

                <div>

                  <h2>
                    🤖 AI Root Cause Analysis
                  </h2>

                  <p>
                    Analysis generated using
                    incident evidence and the
                    OpsMind AI knowledge base.
                  </p>

                </div>

              </div>


              {/* Severity + Confidence */}

              <div className="ai-analysis-grid">

                <div className="ai-analysis-item">

                  <span className="ai-label">
                    Severity
                  </span>

                  <strong>
                    {aiAnalysis.severity}
                  </strong>

                </div>


                <div className="ai-analysis-item">

                  <span className="ai-label">
                    Confidence
                  </span>

                  <strong>
                    {Math.round(
                      aiAnalysis.confidence * 100
                    )}
                    %
                  </strong>

                </div>

              </div>


              {/* Probable Cause */}

              <div className="ai-section">

                <h3>
                  Probable Cause
                </h3>

                <p>
                  {aiAnalysis.probable_cause}
                </p>

              </div>


              {/* Recommendations */}

              <div className="ai-section">

                <h3>
                  Recommendations
                </h3>

                <p>
                  {aiAnalysis.recommendations}
                </p>

              </div>


              {/* Analysis timestamp */}

              {aiAnalysis.created_at && (

                <div className="ai-analysis-time">

                  Analysis generated on{" "}

                  {new Date(
                    aiAnalysis.created_at
                  ).toLocaleString()}

                </div>

              )}

            </section>

          )}


          {/* ==========================================
              DESCRIPTION
          ========================================== */}

          <section className="detail-card">

            <div className="detail-card-header">

              <FileText size={20} />

              <h3>
                Description
              </h3>

            </div>

            <p>
              {incident.description}
            </p>

          </section>


          {/* ==========================================
              INFORMATION
          ========================================== */}

          <div className="detail-info-grid">

            <div className="detail-info-card">

              <Server size={20} />

              <div>

                <span>
                  Service
                </span>

                <strong>
                  {incident.serviceName}
                </strong>

              </div>

            </div>


            <div className="detail-info-card">

              <Clock size={20} />

              <div>

                <span>
                  Created
                </span>

                <strong>
                  {new Date(
                    incident.created_at
                  ).toLocaleString()}
                </strong>

              </div>

            </div>

          </div>


          {/* ==========================================
              LOGS
          ========================================== */}

          <section className="detail-card">

            <div className="detail-card-header">

              <FileText size={20} />

              <h3>
                Logs
              </h3>

            </div>


            {incident.logs &&
            incident.logs.length > 0 ? (

              <div className="logs-list">

                {incident.logs.map(
                  (log) => (

                    <div
                      className="log-entry"
                      key={log.id}
                    >

                      <span className="log-level">
                        {log.level}
                      </span>

                      <span>
                        {log.message}
                      </span>

                    </div>

                  )
                )}

              </div>

            ) : (

              <p>
                No logs available for
                this incident.
              </p>

            )}

          </section>


          {/* ==========================================
              COMMENTS
          ========================================== */}

          <section className="detail-card">

            <div className="detail-card-header">

              <FileText size={20} />

              <h3>
                Comments
              </h3>

            </div>


            {incident.comments &&
            incident.comments.length > 0 ? (

              <div className="comments-list">

                {incident.comments.map(
                  (comment) => (

                    <div
                      className="comment-entry"
                      key={comment.id}
                    >

                      <strong>
                        User #{comment.user_id}
                      </strong>

                      <p>
                        {comment.comment}
                      </p>

                    </div>

                  )
                )}

              </div>

            ) : (

              <p>
                No comments yet.
              </p>

            )}

          </section>
          

          <section className="detail-card">

  <div className="detail-card-header">

    <Clock size={20} />

    <h3>
      Incident Timeline
    </h3>

  </div>


  {timelineLoading ? (

    <p>
      Loading timeline...
    </p>

  ) : timeline.length > 0 ? (

    <div className="incident-timeline">

      {timeline.map((event, index) => (

        <div
          className="timeline-item"
          key={`${event.event_type}-${event.timestamp}-${index}`}
        >

          <div className="timeline-marker">
            <div className="timeline-dot"></div>

            {index <
              timeline.length - 1 && (
                <div className="timeline-line"></div>
            )}

          </div>


          <div className="timeline-content">

            <div className="timeline-event-type">
              {event.event_type
                ?.replaceAll("_", " ")}
            </div>


            <p className="timeline-description">
              {event.description}
            </p>


            <span className="timeline-time">

              {new Date(
                event.timestamp
              ).toLocaleString()}

            </span>

          </div>

        </div>

      ))}

    </div>

  ) : (

    <p>
      No timeline events available.
    </p>

  )}

</section>

        </section>
      </main>
    </div>

    
  );
}

export default IncidentDetails;