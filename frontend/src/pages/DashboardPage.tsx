import { useAuth } from "../context/AuthContext";
import RequirePermission from "../components/RequirePermission";

export default function DashboardPage() {
  const { user } = useAuth();

  return (
    <div style={{ padding: "24px" }}>
      <h1>Dashboard</h1>
      <p>Welcome, {user?.full_name}!</p>
      <p>Role: <strong>{user?.role}</strong></p>

      <RequirePermission claim="dashboard.view">
        <section style={{ marginTop: "16px", padding: "16px", border: "1px solid #ccc", borderRadius: "8px" }}>
          <h2>Dashboard Overview</h2>
          <p>You can view the dashboard.</p>
        </section>
      </RequirePermission>

      <RequirePermission claim="dashboard.edit">
        <section style={{ marginTop: "16px", padding: "16px", border: "1px solid #ccc", borderRadius: "8px" }}>
          <h2>Edit Dashboard</h2>
          <p>You have edit access to the dashboard.</p>
        </section>
      </RequirePermission>

      <RequirePermission claim="settings.view">
        <section style={{ marginTop: "16px", padding: "16px", border: "1px solid #ccc", borderRadius: "8px" }}>
          <h2>Settings</h2>
          <p>You can view settings.</p>
        </section>
      </RequirePermission>

      <RequirePermission claim="settings.edit">
        <section style={{ marginTop: "16px", padding: "16px", border: "1px solid #ccc", borderRadius: "8px" }}>
          <h2>Edit Settings</h2>
          <p>You have edit access to settings.</p>
        </section>
      </RequirePermission>

      <RequirePermission claim="users.view">
        <section style={{ marginTop: "16px", padding: "16px", border: "1px solid #ccc", borderRadius: "8px" }}>
          <h2>Users</h2>
          <p>You can view the user list.</p>
        </section>
      </RequirePermission>

      <RequirePermission claim="users.manage">
        <section style={{ marginTop: "16px", padding: "16px", border: "1px solid #ccc", borderRadius: "8px" }}>
          <h2>Manage Users</h2>
          <p>You can manage users.</p>
        </section>
      </RequirePermission>
    </div>
  );
}
