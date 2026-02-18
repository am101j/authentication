import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, loading } = useAuth();

  return (
    <nav className="navbar">
      <span className="navbar-brand">SSO App</span>
      <div className="navbar-user">
        {loading ? (
          <span>Loading...</span>
        ) : user ? (
          <>
            <span>{user.full_name} ({user.roles.join(", ") || "No roles"})</span>
            <a href="/auth/logout">Logout</a>
          </>
        ) : null}
      </div>
    </nav>
  );
}
