import { useAuth } from "../context/AuthContext";
import RequireAgent from "../components/RequireAgent";

const AGENTS = [
  { name: "Design Agent", slug: "design-agent", description: "AI-powered design assistance for your projects." },
  { name: "Developer Agent", slug: "developer-agent", description: "AI-powered development assistance and code generation." },
  { name: "Testing Agent", slug: "testing-agent", description: "AI-powered testing and quality assurance." },
];

export default function AgentsPage() {
  const { user } = useAuth();

  return (
    <div className="agents-page">
      <div className="agents-header">
        <h1>Agents</h1>
        <p>Welcome, {user?.full_name}!</p>
      </div>

      {user?.agents.length === 0 && (
        <div className="no-agents">
          <p>No agents available. Contact an administrator to assign roles to your account.</p>
        </div>
      )}

      <div className="token-debug">
        <div className="token-debug-title">Raw Entra identity (what Microsoft gives us)</div>
        <pre>{JSON.stringify({
          oid: user?.entra_oid,
          preferred_username: user?.email,
          name: user?.full_name,
        }, null, 2)}</pre>
      </div>

      <div className="token-debug">
        <div className="token-debug-title">Resolved session (after looking up roles and agents in our DB)</div>
        <pre>{JSON.stringify({
          id: user?.id,
          email: user?.email,
          full_name: user?.full_name,
          roles: user?.roles,
          agents: user?.agents,
        }, null, 2)}</pre>
      </div>

      <div className="agents-grid">
        {AGENTS.map((agent) => (
          <RequireAgent key={agent.slug} slug={agent.slug}>
            <div className="agent-card">
              <h2>{agent.name}</h2>
              <p>{agent.description}</p>
            </div>
          </RequireAgent>
        ))}
      </div>
    </div>
  );
}
