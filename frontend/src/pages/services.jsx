import { useEffect, useState } from "react";

import {
  Server,
  CheckCircle,
  XCircle,
  AlertTriangle,
  RefreshCw,
} from "lucide-react";

import "../Dashboard.css";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import api from "../services/api";


function Services() {

  const [services, setServices] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");


  useEffect(() => {
    loadServices();
  }, []);


  const loadServices = async () => {

    try {

      setLoading(true);
      setError("");

      const response = await api.get("/services");

      setServices(response.data);

    } catch (error) {

      console.error(
        "Failed to load services:",
        error
      );

      setError(
        "Unable to load services."
      );

    } finally {

      setLoading(false);

    }

  };


  const getStatusIcon = (status) => {

    if (status === "OPERATIONAL") {
      return <CheckCircle size={22} />;
    }

    if (status === "DOWN") {
      return <XCircle size={22} />;
    }

    return <AlertTriangle size={22} />;

  };


  const getStatusClass = (status) => {

    if (status === "OPERATIONAL") {
      return "operational";
    }

    if (status === "DOWN") {
      return "down";
    }

    return "warning";

  };


  return (

    <div className="dashboard-layout">

      <Sidebar />


      <main className="dashboard-main">

        <Navbar />


        <section className="dashboard-content">


          {/* Page Header */}

          <div className="welcome-section">

            <h2>
              Services
            </h2>

            <p>
              Monitor the health and status of
              your infrastructure services.
            </p>

          </div>


          {/* Loading */}

          {loading && (

            <div className="services-message">

              <RefreshCw
                size={20}
                className="loading-icon"
              />

              <p>
                Loading services...
              </p>

            </div>

          )}


          {/* Error */}

          {!loading && error && (

            <div className="services-message error-message">

              <XCircle size={20} />

              <p>
                {error}
              </p>

              <button
                className="view-all-button"
                onClick={loadServices}
              >
                Retry
              </button>

            </div>

          )}


          {/* Empty */}

          {!loading &&
            !error &&
            services.length === 0 && (

              <div className="services-message">

                <Server size={24} />

                <p>
                  No services found.
                </p>

              </div>

            )}


          {/* Services */}

          {!loading &&
            !error &&
            services.length > 0 && (

              <div className="services-grid">

                {services.map((service) => (

                  <div
                    className="service-card"
                    key={service.id}
                  >


                    {/* Card Header */}

                    <div className="service-card-header">

                      <div className="service-icon">

                        <Server size={24} />

                      </div>


                      <div>

                        <h3>
                          {service.name}
                        </h3>

                        <span>
                          Service #{service.id}
                        </span>

                      </div>

                    </div>


                    {/* Description */}

                    <p className="service-description">

                      {service.description ||
                        "No description available."}

                    </p>


                    {/* Status */}

                    <div className="service-status-row">

                      <span>
                        Status
                      </span>


                      <div
                        className={`service-status ${getStatusClass(
                          service.status
                        )}`}
                      >

                        {getStatusIcon(
                          service.status
                        )}

                        <span>
                          {service.status}
                        </span>

                      </div>

                    </div>


                    {/* Created */}

                    <div className="service-created">

                      Created{" "}

                      {new Date(
                        service.created_at
                      ).toLocaleDateString()}

                    </div>

                  </div>

                ))}

              </div>

            )}

        </section>

      </main>

    </div>

  );
}


export default Services;