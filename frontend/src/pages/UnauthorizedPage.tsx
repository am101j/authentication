import { Link } from "react-router-dom";

export default function UnauthorizedPage() {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", minHeight: "60vh" }}>
      <h1>Access Denied</h1>
      <p>You do not have permission to view this page.</p>
      <Link to="/">Go to Dashboard</Link>
    </div>
  );
}
