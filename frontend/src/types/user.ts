export interface User {
  id: number;
  entra_oid: string;
  email: string;
  full_name: string;
  roles: string[];
  agents: string[];
}
