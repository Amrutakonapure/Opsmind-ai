import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Incidents from "./pages/Incidents";
import IncidentDetails from "./pages/IncidentDetails";
import Services from "./pages/services";
import AIAnalysis from "./pages/AIAnalysis";

function ProtectedRoute({ children }) {
  const token = localStorage.getItem("token");

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/incidents"
          element={
            <ProtectedRoute>
              <Incidents />
            </ProtectedRoute>
          }
        />

        <Route
          path="/incidents/:id"
          element={
            <ProtectedRoute>
              <IncidentDetails />
            </ProtectedRoute>
          }
          />

          <Route
            path="/ai-analysis"
            element={<AIAnalysis />}
          />

        <Route
          path="/services"
          element={<Services />}
        />

        <Route
          path="/"
          element={<Navigate to="/login" replace />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;