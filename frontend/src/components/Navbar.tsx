import { useAuth } from "../context/AuthContext";
import LoginButton from "./LoginButton";

export default function Navbar() {
  const { user, loading } = useAuth();

  return (
    <nav style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px 24px", borderBottom: "1px solid #ddd" }}>
      <strong>SSO App</strong>
      <div>
        {loading ? (
          <span>Loading...</span>
        ) : user ? (
          <span>
            {user.full_name} ({user.role}){" "}
            <a href="/auth/logout">Logout</a>
          </span>
        ) : (
          <LoginButton />
        )}
      </div>
    </nav>
  );
}
