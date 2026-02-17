import LoginButton from "../components/LoginButton";

export default function LoginPage() {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", minHeight: "60vh" }}>
      <h1>Welcome</h1>
      <p>Please sign in to continue.</p>
      <LoginButton />
    </div>
  );
}
