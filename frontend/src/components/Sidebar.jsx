import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  AlertTriangle,
  Server,
  Brain,
  Sparkles,
  BarChart3,
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
          to="/analytics"
          className={({ isActive }) =>
            isActive ? "nav-item active" : "nav-item"
          }
        >
          <BarChart3 size={20} />
          <span>Analytics</span>
        </NavLink>

        <NavLink
          to="/ai-analysis"
          className="nav-item"
        >
          <Brain size={20} />
          <span>AI Analysis</span>
        </NavLink>

        <NavLink
          to="/ai-assistant"
          className={({ isActive }) =>
          isActive ? "nav-item active" : "nav-item"
          }
        >
          <Sparkles size={20} />
          <span>AI Assistant</span>
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