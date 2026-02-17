import { loginRedirect } from "../api/auth";

export default function LoginButton() {
  return (
    <button onClick={loginRedirect} style={{ padding: "10px 24px", fontSize: "16px", cursor: "pointer" }}>
      Sign in with Microsoft
    </button>
  );
}
