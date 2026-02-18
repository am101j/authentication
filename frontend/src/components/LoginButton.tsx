import { loginRedirect } from "../api/auth";

export default function LoginButton() {
  return (
    <>
      <button onClick={loginRedirect} className="btn-primary">
        Sign in with Microsoft
      </button>
      <div className="dev-login">
        <span>Mock Entra:</span>
        <a href="/auth/dev-login?user_id=1">Alice</a>
        <a href="/auth/dev-login?user_id=2">Bob</a>
        <a href="/auth/dev-login?user_id=3">Carol</a>
      </div>
    </>
  );
}
