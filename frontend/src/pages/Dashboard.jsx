import { useEffect, useState } from "react";

import {
  AlertTriangle,
  Activity,
  Brain,
  CheckCircle,
} from "lucide-react";

import "../Dashboard.css";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import StatCard from "../components/StatCard";
import IncidentCard from "../components/IncidentCard";
import api from "../services/api";

function Dashboard() {

  const [stats, setStats] = useState({
    total: 0,
    open: 0,
    critical: 0,
    resolved: 0,
    aiAnalyses: "—",
  });

  const [incidents, setIncidents] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");


  useEffect(() => {
    loadDashboard();
  }, []);


  const loadDashboard = async () => {

    try {

      setLoading(true);
      setError("");

      const [
        statsResponse,
        incidentsResponse,
        servicesResponse,
      ] = await Promise.all([
        api.get("/incidents/stats"),
        api.get("/incidents?limit=5"),
        api.get("/services"),
      ]);


      const backendStats = statsResponse.data;
      const backendIncidents = incidentsResponse.data;
      const backendServices = servicesResponse.data;


      /*
       * Convert service IDs into service names.
       */
      const formattedIncidents = backendIncidents.map(
        (incident) => {

          const service = backendServices.find(
            (service) =>
              service.id === incident.service_id
          );

          return {
            id: incident.id,
            title: incident.title,
            service:
              service?.name ||
              `Service #${incident.service_id}`,
            severity: incident.severity,
            status: incident.status,
          };

        }
      );


      setStats({
        total: backendStats.total ?? 0,

        open: backendStats.open ?? 0,

        critical: backendStats.critical ?? 0,

        resolved: backendStats.resolved ?? 0,

        /*
         * The current backend statistics endpoint
         * does not provide an AI analysis count.
         */
        aiAnalyses: "—",
      });


      setIncidents(formattedIncidents);

    } catch (error) {

      console.error(
        "Dashboard loading failed:",
        error
      );

      setError(
        "Unable to load dashboard data."
      );

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


          {/* =====================================
              WELCOME SECTION
          ===================================== */}

          <div className="welcome-section">

            <h2>
              Welcome back, Admin 👋
            </h2>

            <p>
              Here's what's happening across
              your infrastructure.
            </p>

          </div>



          {/* =====================================
              STATISTICS
          ===================================== */}

          <div className="stats-grid">


            <StatCard
              title="Total Incidents"
              value={stats.total}
              description="All reported incidents"
              icon={AlertTriangle}
            />


            <StatCard
              title="Open Incidents"
              value={stats.open}
              description="Currently being investigated"
              icon={Activity}
            />


            <StatCard
              title="Critical Incidents"
              value={stats.critical}
              description="Require immediate attention"
              icon={AlertTriangle}
            />


            <StatCard
              title="Resolved Incidents"
              value={stats.resolved}
              description="Successfully resolved"
              icon={CheckCircle}
            />


          </div>



          {/* =====================================
              RECENT INCIDENTS
          ===================================== */}

          <section className="recent-incidents">


            <div className="section-header">

              <div>

                <h2>
                  Recent Incidents
                </h2>

                <p>
                  Latest system incidents
                </p>

              </div>


              <button
                className="view-all-button"
                onClick={() => {
                  window.location.href =
                    "/incidents";
                }}
              >
                View All
              </button>

            </div>



            <div className="incident-list">


              {/* Loading */}

              {loading && (

                <p>
                  Loading incidents...
                </p>

              )}



              {/* Error */}

              {!loading &&
                error && (

                  <p>
                    {error}
                  </p>

                )}



              {/* Empty */}

              {!loading &&
                !error &&
                incidents.length === 0 && (

                  <p>
                    No incidents found.
                  </p>

                )}



              {/* Incidents */}

              {!loading &&
                !error &&
                incidents.length > 0 && (

                  incidents.map(
                    (incident) => (

                      <IncidentCard
                        key={incident.id}
                        incident={incident}
                      />

                    )
                  )

                )}

            </div>

          </section>


        </section>

      </main>

    </div>

  );
}

export default Dashboard;