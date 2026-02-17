import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import type { User } from "../types/user";
import { fetchCurrentUser } from "../api/auth";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  hasPermission: (slug: string) => boolean;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
  hasPermission: () => false,
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCurrentUser()
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  const hasPermission = (slug: string): boolean => {
    if (!user) return false;
    return user.permissions.includes(slug);
  };

  return (
    <AuthContext.Provider value={{ user, loading, hasPermission }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  return useContext(AuthContext);
}
