import { useNavigate } from "react-router-dom";

function IncidentCard({ incident }) {

  const navigate = useNavigate();

  return (

    <div
      className="incident-card clickable"
      onClick={() =>
        navigate(`/incidents/${incident.id}`)
      }
    >

      <div className="incident-main">

        <div>

          <h3>
            {incident.title}
          </h3>

          <p>
            {incident.service}
          </p>

        </div>


        <span
          className={`severity-badge ${incident.severity.toLowerCase()}`}
        >
          {incident.severity}
        </span>

      </div>


      <div className="incident-footer">

        <span>
          Status: {incident.status}
        </span>

        <span>
          #{incident.id}
        </span>

      </div>

    </div>

  );
}

export default IncidentCard;