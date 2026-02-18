# SSO Service

Single Sign-On app with Microsoft Entra ID authentication and role-based agent access control.

**Stack:** FastAPI · React + TypeScript · SQLite (dev) / PostgreSQL (prod) · MSAL

---

## Running locally (no Docker needed)

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1. Clone the repo
```bash
git clone <repo-url>
cd sso
```

### 2. Backend setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

### 3. Create your .env file
Create `backend/.env` with the following (for local dev, Entra credentials are optional):
```
DATABASE_URL=sqlite+aiosqlite:///./sso.db
JWT_SECRET=any-random-string-here
FRONTEND_URL=http://localhost:5173
```

### 4. Seed the database
This creates all tables and inserts test users, roles, and agents:
```bash
python -m app.seed
```

### 5. Start the backend
```bash
uvicorn app.main:app --reload --port 8000
```
Runs on http://localhost:8000

### 6. Start the frontend (new terminal)
```bash
cd frontend
npm install
npm run dev
```
Runs on http://localhost:5173

---

## Logging in (dev)

The login page has **Mock Entra** shortcuts — no Microsoft account needed:

| Link | User | Roles | Sees |
|------|------|-------|------|
| Alice | alice@localhost | Deposit Tester | Testing Agent |
| Bob | bob@localhost | Developer | Developer Agent |
| Carol | carol@localhost | Deposit Design, Developer | Design Agent, Developer Agent |

Or hit directly: `http://localhost:8000/auth/dev-login?user_id=1`

---

## How it works

1. User clicks a dev login link → backend looks up that user in the DB
2. Backend reads their roles → figures out which agents those roles unlock
3. Backend creates a signed JWT containing their name, roles, and agents
4. JWT is stored as a cookie (`sso_token`) in the browser
5. Frontend calls `/api/user/me` → backend decodes the cookie → returns user info
6. Frontend shows only the agent cards the user has access to

---

## Roles and agents

| Role | Agent unlocked |
|------|---------------|
| Deposit Tester | Testing Agent |
| Deposit Design | Design Agent |
| Lending Tester | Testing Agent |
| Developer | Developer Agent |

---

## Using real Microsoft Entra (production)

Add to `backend/.env`:
```
ENTRA_CLIENT_ID=your-client-id
ENTRA_CLIENT_SECRET=your-client-secret
ENTRA_TENANT_ID=your-tenant-id
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/sso
```

Users must be pre-created in the database with their Entra `oid` set. Unknown users are rejected at login.

Run migrations against Postgres:
```bash
alembic upgrade head
python -m app.seed
```
