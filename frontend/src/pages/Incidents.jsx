import { useEffect, useState } from "react";
import { Search, Plus, X } from "lucide-react";

import "../Dashboard.css";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import IncidentCard from "../components/IncidentCard";
import api from "../services/api";

function Incidents() {

  const [incidents, setIncidents] = useState([]);

  const [services, setServices] = useState([]);

  const [search, setSearch] = useState("");

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  const [showCreateForm, setShowCreateForm] = useState(false);

  const [creating, setCreating] = useState(false);

  const [createError, setCreateError] = useState("");

  const [formData, setFormData] = useState({
    title: "",
    description: "",
    severity: "MEDIUM",
    service_id: "",
  });


  useEffect(() => {
    loadIncidents();
  }, []);


  const loadIncidents = async () => {

    try {

      setLoading(true);
      setError("");

      const [
        incidentsResponse,
        servicesResponse,
      ] = await Promise.all([
        api.get("/incidents?limit=50"),
        api.get("/services"),
      ]);


      const backendIncidents =
        incidentsResponse.data;

      const backendServices =
        servicesResponse.data;


      setServices(backendServices);


      setIncidents(
        backendIncidents.map((incident) => {

          const service =
            backendServices.find(
              (service) =>
                service.id === incident.service_id
            );

          return {
            ...incident,

            serviceName:
              service?.name ||
              `Service #${incident.service_id}`,
          };

        })
      );

    } catch (error) {

      console.error(
        "Failed to load incidents:",
        error
      );

      setError(
        "Unable to load incidents."
      );

    } finally {

      setLoading(false);

    }
  };


  const handleFormChange = (event) => {

    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));

  };


  const handleCreateIncident = async (event) => {

    event.preventDefault();

    try {

      setCreating(true);
      setCreateError("");


      if (!formData.title.trim()) {

        setCreateError(
          "Incident title is required."
        );

        return;
      }


      if (!formData.description.trim()) {

        setCreateError(
          "Incident description is required."
        );

        return;
      }


      if (!formData.service_id) {

        setCreateError(
          "Please select a service."
        );

        return;
      }


      const newIncident = {

        title: formData.title.trim(),

        description:
          formData.description.trim(),

        severity: formData.severity,

        status: "OPEN",

        service_id:
          Number(formData.service_id),

        assigned_to: null,

      };


      await api.post(
        "/incidents",
        newIncident
      );


      setFormData({
        title: "",
        description: "",
        severity: "MEDIUM",
        service_id: "",
      });


      setShowCreateForm(false);


      await loadIncidents();

    } catch (error) {

      console.error(
        "Failed to create incident:",
        error
      );


      const backendMessage =
        error.response?.data?.detail;


      setCreateError(
        backendMessage ||
        "Unable to create incident."
      );

    } finally {

      setCreating(false);

    }
  };


  const filteredIncidents =
    incidents.filter((incident) =>
      incident.title
        .toLowerCase()
        .includes(search.toLowerCase())
    );


  return (

    <div className="dashboard-layout">

      <Sidebar />


      <main className="dashboard-main">

        <Navbar />


        <section className="dashboard-content">


          <div className="welcome-section">

            <h2>
              Incidents
            </h2>

            <p>
              Monitor and manage system incidents.
            </p>

          </div>


          {/* Search and Create */}

          <div className="incident-toolbar">

            <div className="search-box">

              <Search size={20} />

              <input
                type="text"
                placeholder="Search incidents..."
                value={search}
                onChange={(event) =>
                  setSearch(event.target.value)
                }
              />

            </div>


            <button
              className="create-incident-button"
              onClick={() => {
                setCreateError("");
                setShowCreateForm(true);
              }}
            >

              <Plus size={18} />

              Create Incident

            </button>

          </div>


          {/* Create Incident Form */}

          {showCreateForm && (

            <div className="create-incident-card">

              <div className="create-incident-header">

                <div>

                  <h3>
                    Create New Incident
                  </h3>

                  <p>
                    Report a new infrastructure issue.
                  </p>

                </div>


                <button
                  className="close-form-button"
                  onClick={() =>
                    setShowCreateForm(false)
                  }
                >
                  <X size={20} />
                </button>

              </div>


              <form
                onSubmit={handleCreateIncident}
              >


                {/* Title */}

                <div className="form-group">

                  <label>
                    Incident Title
                  </label>

                  <input
                    type="text"
                    name="title"
                    placeholder="e.g. Payment gateway timeout"
                    value={formData.title}
                    onChange={handleFormChange}
                  />

                </div>


                {/* Description */}

                <div className="form-group">

                  <label>
                    Description
                  </label>

                  <textarea
                    name="description"
                    placeholder="Describe what is happening..."
                    value={formData.description}
                    onChange={handleFormChange}
                    rows="5"
                  />

                </div>


                <div className="form-row">


                  {/* Severity */}

                  <div className="form-group">

                    <label>
                      Severity
                    </label>

                    <select
                      name="severity"
                      value={formData.severity}
                      onChange={handleFormChange}
                    >

                      <option value="LOW">
                        LOW
                      </option>

                      <option value="MEDIUM">
                        MEDIUM
                      </option>

                      <option value="HIGH">
                        HIGH
                      </option>

                      <option value="CRITICAL">
                        CRITICAL
                      </option>

                    </select>

                  </div>


                  {/* Service */}

                  <div className="form-group">

                    <label>
                      Service
                    </label>

                    <select
                      name="service_id"
                      value={formData.service_id}
                      onChange={handleFormChange}
                    >

                      <option value="">
                        Select a service
                      </option>


                      {services.map((service) => (

                        <option
                          key={service.id}
                          value={service.id}
                        >
                          {service.name}
                        </option>

                      ))}

                    </select>

                  </div>

                </div>


                {/* Error */}

                {createError && (

                  <div className="form-error">
                    {createError}
                  </div>

                )}


                {/* Buttons */}

                <div className="form-actions">

                  <button
                    type="button"
                    className="cancel-button"
                    onClick={() =>
                      setShowCreateForm(false)
                    }
                  >
                    Cancel
                  </button>


                  <button
                    type="submit"
                    className="submit-incident-button"
                    disabled={creating}
                  >

                    {creating
                      ? "Creating..."
                      : "Create Incident"}

                  </button>

                </div>

              </form>

            </div>

          )}


          {/* Incident List */}

          <div className="incident-page-list">

            {loading && (
              <p>
                Loading incidents...
              </p>
            )}


            {!loading && error && (
              <p>
                {error}
              </p>
            )}


            {!loading &&
              !error &&
              filteredIncidents.length === 0 && (

                <p>
                  No incidents found.
                </p>

              )}


            {!loading &&
              !error &&
              filteredIncidents.map(
                (incident) => (

                  <IncidentCard
                    key={incident.id}
                    incident={{
                      id: incident.id,
                      title: incident.title,
                      service: incident.serviceName,
                      severity: incident.severity,
                      status: incident.status,
                    }}
                  />

                )
              )}

          </div>

        </section>

      </main>

    </div>

  );
}

export default Incidents;