import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  AlertTriangle,
  Server,
  Brain,
  LogOut,
} from "lucide-react";

function Sidebar() {
  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
  };

  return (
    <aside className="sidebar">

      <div className="sidebar-logo">
        <div className="logo-box">OM</div>

        <div>
          <h2>OpsMind</h2>
          <span>AI</span>
        </div>
      </div>

      <nav className="sidebar-nav">

        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            isActive ? "nav-item active" : "nav-item"
          }
        >
          <LayoutDashboard size={20} />
          <span>Dashboard</span>
        </NavLink>

        <NavLink
          to="/incidents"
          className="nav-item"
        >
          <AlertTriangle size={20} />
          <span>Incidents</span>
        </NavLink>

        <NavLink
          to="/services"
          className="nav-item"
        >
          <Server size={20} />
          <span>Services</span>
        </NavLink>

        <NavLink
          to="/ai-analysis"
          className="nav-item"
        >
          <Brain size={20} />
          <span>AI Analysis</span>
        </NavLink>

      </nav>

      <button className="logout-button" onClick={handleLogout}>
        <LogOut size={20} />
        <span>Logout</span>
      </button>

    </aside>
  );
}

export default Sidebar;