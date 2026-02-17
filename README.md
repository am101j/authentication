# SSO Service

Single Sign-On app with Microsoft Entra ID authentication and role-based access control (RBAC).

**Stack:** FastAPI · React + TypeScript · PostgreSQL · MSAL

## Setup

### 1. Prerequisites
- Python 3.10+
- Node.js 18+
- Docker

### 2. Start the database
```bash
docker-compose up -d
```

### 3. Configure environment
Copy `.env.example` to `backend/.env` and fill in your Microsoft Entra ID credentials:
```
ENTRA_CLIENT_ID=your-client-id
ENTRA_CLIENT_SECRET=your-client-secret
ENTRA_TENANT_ID=your-tenant-id
```

### 4. Run the backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload
```
Runs on http://localhost:8000

### 5. Run the frontend
```bash
cd frontend
npm install
npm run dev
```
Runs on http://localhost:5173

## How it works
1. User clicks Login → redirected to Microsoft
2. Microsoft authenticates → redirects back with identity
3. Backend creates user (default "Guest" role) or finds existing one
4. Backend issues a JWT cookie with role + permissions
5. Frontend reads the JWT to show/hide UI based on permissions

## Roles
| Role  | Permissions |
|-------|-------------|
| Admin | dashboard.view, dashboard.edit, settings.view, settings.edit, users.view, users.manage |
| User  | dashboard.view, dashboard.edit, settings.view |
| Guest | dashboard.view |
