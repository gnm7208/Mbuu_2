import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

export default function ProtectedRoute({ children, role }) {
  const { user } = useContext(AuthContext);
  if (!user) return <Navigate to="/login" replace />;
  if (role === "admin" && !user.is_admin) return <Navigate to="/" replace />;
  if (role === "customer" && user.is_admin) return <Navigate to="/" replace />;
  return children;
}
