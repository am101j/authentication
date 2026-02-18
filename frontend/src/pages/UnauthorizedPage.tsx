import { Link } from "react-router-dom";

export default function UnauthorizedPage() {
  return (
    <div className="unauthorized-page">
      <h1>Access Denied</h1>
      <p>You do not have permission to view this page.</p>
      <Link to="/">Go to Dashboard</Link>
    </div>
  );
}
