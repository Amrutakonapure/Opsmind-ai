import { Bell, UserCircle } from "lucide-react";

function Navbar() {
  return (
    <header className="navbar">

      <div>
        <h1>Operations Dashboard</h1>
        <p>Monitor incidents and system health</p>
      </div>

      <div className="navbar-right">

        <button className="icon-button">
          <Bell size={21} />
        </button>

        <div className="user-profile">
          <UserCircle size={32} />

          <div>
            <strong>Admin</strong>
            <span>Administrator</span>
          </div>
        </div>

      </div>

    </header>
  );
}

export default Navbar;