import { useState } from "react";
import {
  Brain,
  AlertTriangle,
  CheckCircle,
  Lightbulb,
  Loader,
} from "lucide-react";

import "../Dashboard.css";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import api from "../services/api";

function AIAnalysis() {
  const [incidentId, setIncidentId] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!incidentId) {
      setError("Please enter an incident ID.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setAnalysis(null);

      const response = await api.post(
        `/ai/incidents/${incidentId}/analyze`
      );

      setAnalysis(response.data);
    } catch (error) {
      console.error("AI analysis failed:", error);

      const message =
        error.response?.data?.detail ||
        "Unable to analyze this incident.";

      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-layout">

      <Sidebar />

      <main className="dashboard-main">

        <Navbar />

        <section className="dashboard-content">

          <div className="welcome-section">

            <h2>
              AI Incident Analysis
            </h2>

            <p>
              Use OpsMind AI to investigate an incident
              and identify its probable root cause.
            </p>

          </div>


          {/* Analysis Input */}

          <section className="detail-card">

            <div className="detail-card-header">

              <Brain size={22} />

              <h3>
                Analyze an Incident
              </h3>

            </div>


            <p>
              Enter an incident ID to generate an
              AI-powered root cause analysis.
            </p>


            <div className="ai-analysis-input">

              <input
                type="number"
                placeholder="Enter Incident ID"
                value={incidentId}
                onChange={(e) =>
                  setIncidentId(e.target.value)
                }
              />


              <button
                onClick={handleAnalyze}
                disabled={loading}
              >

                {loading ? (
                  <>
                    <Loader size={18} />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Brain size={18} />
                    Analyze Incident
                  </>
                )}

              </button>

            </div>


            {error && (

              <div className="ai-error">

                <AlertTriangle size={18} />

                <span>
                  {error}
                </span>

              </div>

            )}

          </section>


          {/* AI Result */}

          {analysis && (

            <section className="ai-analysis-result">

              <div className="ai-analysis-title">

                <Brain size={26} />

                <div>

                  <h2>
                    AI Root Cause Analysis
                  </h2>

                  <p>
                    Analysis generated using incident
                    evidence and the OpsMind AI
                    knowledge base.
                  </p>

                </div>

              </div>


              {/* Severity + Confidence */}

              <div className="ai-summary-grid">

                <div className="ai-summary-card">

                  <AlertTriangle size={22} />

                  <span>
                    Severity
                  </span>

                  <strong
                    className={`severity-badge ${
                      analysis.severity.toLowerCase()
                    }`}
                  >
                    {analysis.severity}
                  </strong>

                </div>


                <div className="ai-summary-card">

                  <CheckCircle size={22} />

                  <span>
                    Confidence
                  </span>

                  <strong>
                    {Math.round(
                      analysis.confidence * 100
                    )}
                    %
                  </strong>

                </div>

              </div>


              {/* Probable Cause */}

              <div className="detail-card">

                <div className="detail-card-header">

                  <AlertTriangle size={20} />

                  <h3>
                    Probable Cause
                  </h3>

                </div>

                <p>
                  {analysis.probable_cause}
                </p>

              </div>


              {/* Recommendations */}

              <div className="detail-card">

                <div className="detail-card-header">

                  <Lightbulb size={20} />

                  <h3>
                    Recommendations
                  </h3>

                </div>

                <p className="recommendations-text">
                  {analysis.recommendations}
                </p>

              </div>


              {/* Timestamp */}

              <p className="analysis-timestamp">

                Analysis generated on{" "}

                {new Date(
                  analysis.created_at
                ).toLocaleString()}

              </p>

            </section>

          )}

        </section>

      </main>

    </div>
  );
}

export default AIAnalysis;