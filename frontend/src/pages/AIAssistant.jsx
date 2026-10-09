import { useState } from "react";
import { Brain, Send, Loader2, FileText, AlertCircle } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import "../Dashboard.css";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import api from "../services/api";

function AIAssistant() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAsk = async (event) => {
    event.preventDefault();

    if (!question.trim()) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setAnswer("");
      setSources([]);

      const response = await api.get("/rag/ask", {
        params: {
          question: question.trim(),
          limit: 5,
        },
      });

      setAnswer(response.data.answer || "");
      setSources(response.data.sources || []);
    } catch (error) {
      console.error("RAG request failed:", error);

      const message =
        error.response?.data?.detail ||
        "Unable to get an answer from the AI assistant.";

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

        <div className="dashboard-content">
          <div className="page-header">
            <div>
              <h1>AI Assistant</h1>
              <p>
                Ask questions about incidents, services, logs, and operational
                knowledge.
              </p>
            </div>
          </div>

          <div className="ai-assistant-card">
            <div className="ai-assistant-header">
              <div className="ai-assistant-icon">
                <Brain size={28} />
              </div>

              <div>
                <h2>OpsMind AI Assistant</h2>
                <p>
                  Powered by RAG, semantic search, and your incident knowledge
                  base.
                </p>
              </div>
            </div>

            <form onSubmit={handleAsk} className="ai-question-form">
              <textarea
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                placeholder="Ask something like: What could cause repeated payment gateway timeouts?"
                rows={4}
              />

              <button
                type="submit"
                className="ai-ask-button"
                disabled={loading || !question.trim()}
              >
                {loading ? (
                  <>
                    <Loader2 size={18} className="spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Send size={18} />
                    Ask AI
                  </>
                )}
              </button>
            </form>

            {error && (
              <div className="ai-error">
                <AlertCircle size={20} />
                <span>{error}</span>
              </div>
            )}

            {answer && (
              <section className="ai-answer-section">
                <div className="section-title">
                  <Brain size={20} />
                  <h3>AI Answer</h3>
                </div>

                <div className="ai-answer">
                   <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {answer.replace(/<br\s*\/?>/gi, "\n")}
                   </ReactMarkdown>
                </div>
              </section>
            )}

            {sources.length > 0 && (
              <section className="ai-sources-section">
                <div className="section-title">
                  <FileText size={20} />
                  <h3>Retrieved Evidence</h3>
                </div>

                <div className="ai-sources">
                  {sources.map((source, index) => (
                    <div
                      className="ai-source-card"
                      key={`${source.chunk_id}-${index}`}
                    >
                      <div className="source-header">
                        <span>Source {index + 1}</span>

                        <span>
                          Distance:{" "}
                          {typeof source.distance === "number"
                            ? source.distance.toFixed(4)
                            : "N/A"}
                        </span>
                      </div>

                      <p>{source.content}</p>

                      <small>
                        Document ID: {source.document_id} • Chunk:{" "}
                        {source.chunk_index}
                      </small>
                    </div>
                  ))}
                </div>
              </section>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default AIAssistant;