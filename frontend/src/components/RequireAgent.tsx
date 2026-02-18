import type { ReactNode } from "react";
import { useAuth } from "../context/AuthContext";

interface Props {
  slug: string;
  children: ReactNode;
  fallback?: ReactNode;
}

export default function RequireAgent({ slug, children, fallback }: Props) {
  const { hasAgentAccess } = useAuth();

  if (!hasAgentAccess(slug)) {
    return fallback ? <>{fallback}</> : null;
  }

  return <>{children}</>;
}
