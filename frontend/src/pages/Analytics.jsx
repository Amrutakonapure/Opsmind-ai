import { useEffect, useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";
import { BarChart3, AlertTriangle, Activity } from "lucide-react";

import "../Dashboard.css";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import api from "../services/api";

function Analytics() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/incidents/stats");

      setStats(response.data);
    } catch (error) {
      console.error("Failed to load analytics:", error);

      setError(
        error.response?.data?.detail ||
          "Unable to load incident analytics."
      );
    } finally {
      setLoading(false);
    }
  };

  const statusData = stats
    ? [
        {
          name: "Open",
          value: stats.open,
        },
        {
          name: "In Progress",
          value: stats.in_progress,
        },
        {
          name: "Resolved",
          value: stats.resolved,
        },
      ]
    : [];

  const severityData = stats
    ? [
        {
          name: "Critical",
          value: stats.critical,
        },
        {
          name: "High",
          value: stats.high,
        },
      ]
    : [];

  return (
    <div className="dashboard-layout">
      <Sidebar />

      <main className="dashboard-main">
        <Navbar />

        <div className="dashboard-content">
          <div className="page-header">
            <div>
              <h1>Analytics</h1>
              <p>
                Monitor incident trends, severity, and operational status.
              </p>
            </div>
          </div>

          {loading && (
            <div className="analytics-message">
              Loading analytics...
            </div>
          )}

          {error && (
            <div className="analytics-error">
              <AlertTriangle size={20} />
              <span>{error}</span>
            </div>
          )}

          {!loading && !error && stats && (
            <>
              <div className="analytics-summary">
                <div className="analytics-stat-card">
                  <div className="analytics-stat-icon">
                    <Activity size={22} />
                  </div>

                  <div>
                    <span>Total Incidents</span>
                    <strong>{stats.total}</strong>
                  </div>
                </div>

                <div className="analytics-stat-card">
                  <div className="analytics-stat-icon">
                    <AlertTriangle size={22} />
                  </div>

                  <div>
                    <span>Open Incidents</span>
                    <strong>{stats.open}</strong>
                  </div>
                </div>

                <div className="analytics-stat-card">
                  <div className="analytics-stat-icon">
                    <BarChart3 size={22} />
                  </div>

                  <div>
                    <span>Resolved</span>
                    <strong>{stats.resolved}</strong>
                  </div>
                </div>
              </div>

              <div className="analytics-grid">
                <div className="analytics-card">
                  <div className="analytics-card-header">
                    <div>
                      <h2>Incident Status</h2>
                      <p>Distribution by current incident status.</p>
                    </div>
                  </div>

                  <div className="chart-container">
                    <ResponsiveContainer width="100%" height={320}>
                      <PieChart>
                        <Pie
                          data={statusData}
                          dataKey="value"
                          nameKey="name"
                          cx="50%"
                          cy="50%"
                          outerRadius={105}
                          label
                        >
                          {statusData.map((entry, index) => (
                            <Cell key={`status-${index}`} />
                          ))}
                        </Pie>

                        <Tooltip />
                        <Legend />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                <div className="analytics-card">
                  <div className="analytics-card-header">
                    <div>
                      <h2>Incident Severity</h2>
                      <p>Distribution of high-priority incidents.</p>
                    </div>
                  </div>

                  <div className="chart-container">
                    <ResponsiveContainer width="100%" height={320}>
                      <BarChart data={severityData}>
                        <CartesianGrid strokeDasharray="3 3" />

                        <XAxis dataKey="name" />

                        <YAxis allowDecimals={false} />

                        <Tooltip />

                        <Bar dataKey="value" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      </main>
    </div>
  );
}

export default Analytics;