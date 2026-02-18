import LoginButton from "../components/LoginButton";

export default function LoginPage() {
  return (
    <div className="login-page">
      <div className="login-card">
        <h1>Welcome</h1>
        <p>Please sign in to continue.</p>
        <LoginButton />
      </div>
    </div>
  );
}
