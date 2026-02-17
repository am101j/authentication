import type { ReactNode } from "react";
import { useAuth } from "../context/AuthContext";

interface Props {
  claim: string;
  children: ReactNode;
  fallback?: ReactNode;
}

export default function RequirePermission({ claim, children, fallback }: Props) {
  const { hasPermission } = useAuth();

  if (!hasPermission(claim)) {
    return fallback ? <>{fallback}</> : null;
  }

  return <>{children}</>;
}
