import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ShieldCheck, AlertTriangle } from "lucide-react";

import "../Dashboard.css";
import api from "../services/api";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (event) => {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");

      const formData = new URLSearchParams();

      formData.append("username", email);
      formData.append("password", password);

      const response = await api.post(
        "/auth/login",
        formData,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      const token = response.data.access_token;

      localStorage.setItem("token", token);

      navigate("/dashboard");

    } catch (error) {
      console.error("Login failed:", error);

      const message =
        error.response?.data?.detail ||
        "Invalid email or password.";

      setError(message);

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">

      <div className="login-card">

        <div className="login-icon">
          <ShieldCheck size={32} />
        </div>

        <h1>OpsMind AI</h1>

        <p className="login-subtitle">
          AI-powered incident management
        </p>

        <form onSubmit={handleLogin}>

          <div className="form-group">

            <label>
              Email
            </label>

            <input
              type="email"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              placeholder="Enter your email"
              required
            />

          </div>


          <div className="form-group">

            <label>
              Password
            </label>

            <input
              type="password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              placeholder="Enter your password"
              required
            />

          </div>


          {error && (

            <div className="login-error">

              <AlertTriangle size={18} />

              <span>
                {error}
              </span>

            </div>

          )}


          <button
            type="submit"
            className="login-button"
            disabled={loading}
          >

            {loading
              ? "Signing in..."
              : "Sign In"}

          </button>

        </form>

      </div>

    </div>
  );
}

export default Login;