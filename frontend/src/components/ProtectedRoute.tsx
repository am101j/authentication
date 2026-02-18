import type { ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

interface Props {
  children: ReactNode;
  agent?: string;
}

export default function ProtectedRoute({ children, agent }: Props) {
  const { user, loading, hasAgentAccess } = useAuth();

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (agent && !hasAgentAccess(agent)) {
    return <Navigate to="/unauthorized" replace />;
  }

  return <>{children}</>;
}
