import client from "./client";
import type { User } from "../types/user";

export async function fetchCurrentUser(): Promise<User> {
  const response = await client.get<User>("/api/user/me");
  return response.data;
}

export function loginRedirect(): void {
  window.location.href = "/auth/login";
}
