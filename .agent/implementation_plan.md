# 🏦 NeoVault — FastAPI Server Implementation Plan

## Overview

Build a **FastAPI** backend with **JWT authentication**, **SQLModel ORM** (auto table creation), and full **CRUD operations** for all 8 entities from the database schema.

---

## 📊 Database Schema (from ER Diagram)

### Tables & Relationships

| # | Table          | Key Columns                                                                                          | Relationships                  |
|---|----------------|------------------------------------------------------------------------------------------------------|--------------------------------|
| 1 | **Users**      | id (PK), name, email, password, phone, kyc_status (enum: unverified/verified), created_at            | Has many: Accounts, Bills, Rewards, Budgets, Alerts |
| 2 | **AdminLogs**  | id (PK), admin_id (FK→Users), action, target_type, target_id, timestamp                             | Belongs to: Users              |
| 3 | **Accounts**   | id (PK), user_id (FK→Users), bank_name, account_type (enum: savings/checking/credit_card/loan/investment), masked_account, currency (char3), balance, created_at | Belongs to: Users; Has many: Transactions |
| 4 | **Transactions** | id (PK), account_id (FK→Accounts), description, category, amount, currency (char3), txn_type (enum: debit/credit), merchant, txn_date, posted_date | Belongs to: Accounts          |
| 5 | **Bills**      | id (PK), user_id (FK→Users), biller_name, due_date, amount_due, status (enum: upcoming/paid/overdue), auto_pay, created_at | Belongs to: Users              |
| 6 | **Rewards**    | id (PK), user_id (FK→Users), program_name, points_balance, last_updated                             | Belongs to: Users              |
| 7 | **Budgets**    | id (PK), user_id (FK→Users), month, year, category, limit_amount, spent_amount, created_at          | Belongs to: Users              |
| 8 | **Alerts**     | id (PK), user_id (FK→Users), type (enum: low_balance/bill_due/budget_exceeded), message, created_at  | Belongs to: Users              |

---

## 🗂️ Project Structure

We will restructure the server to follow a clean **domain-driven module pattern**. Each domain gets its own folder with `models.py`, `service.py`, and `controller.py`.

```
server/
├── requirements.txt              # Updated dependencies
├── .env                          # DB + JWT config (gitignored)
├── src/
│   ├── __init__.py
│   ├── main.py                   # FastAPI app + startup (auto table creation)
│   ├── api.py                    # Central router aggregation
│   ├── config.py                 # NEW — Settings via pydantic-settings
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── core.py               # SQLModel engine + session dependency
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── models.py             # Login/Register request/response schemas
│   │   ├── service.py            # JWT create/verify, password hashing
│   │   ├── controller.py         # POST /auth/register, POST /auth/login
│   │   └── dependencies.py       # NEW — get_current_user dependency
│   │
│   ├── users/
│   │   ├── __init__.py
│   │   ├── models.py             # User SQLModel table + request/response schemas
│   │   ├── service.py            # User CRUD logic
│   │   └── controller.py         # GET/PUT/DELETE /users/{id}
│   │
│   ├── accounts/                 # NEW module
│   │   ├── __init__.py
│   │   ├── models.py             # Account SQLModel table + schemas
│   │   ├── service.py            # Account CRUD logic
│   │   └── controller.py         # CRUD /accounts
│   │
│   ├── transactions/             # NEW module
│   │   ├── __init__.py
│   │   ├── models.py             # Transaction SQLModel table + schemas
│   │   ├── service.py            # Transaction CRUD logic
│   │   └── controller.py         # CRUD /transactions
│   │
│   ├── bills/                    # NEW module
│   │   ├── __init__.py
│   │   ├── models.py             # Bill SQLModel table + schemas
│   │   ├── service.py            # Bill CRUD logic
│   │   └── controller.py         # CRUD /bills
│   │
│   ├── rewards/                  # NEW module
│   │   ├── __init__.py
│   │   ├── models.py             # Reward SQLModel table + schemas
│   │   ├── service.py            # Reward CRUD logic
│   │   └── controller.py         # CRUD /rewards
│   │
│   ├── budgets/                  # NEW module
│   │   ├── __init__.py
│   │   ├── models.py             # Budget SQLModel table + schemas
│   │   ├── service.py            # Budget CRUD logic
│   │   └── controller.py         # CRUD /budgets
│   │
│   ├── alerts/                   # NEW module
│   │   ├── __init__.py
│   │   ├── models.py             # Alert SQLModel table + schemas
│   │   ├── service.py            # Alert CRUD logic
│   │   └── controller.py         # CRUD /alerts
│   │
│   ├── admin_logs/               # NEW module
│   │   ├── __init__.py
│   │   ├── models.py             # AdminLog SQLModel table + schemas
│   │   ├── service.py            # AdminLog CRUD logic
│   │   └── controller.py         # CRUD /admin-logs
│   │
│   └── entities/                 # REMOVE (replaced by per-module models)
│       ├── __init__.py
│       ├── user.py
│       └── todo.py
│
└── tests/                        # Future: pytest test files
```

---

## 🔧 Implementation Steps

### Phase 1: Foundation (Steps 1–3)

#### Step 1 — Update Dependencies
Update `requirements.txt` to use **SQLModel** instead of raw SQLAlchemy:

```
fastapi
uvicorn[standard]
python-dotenv
sqlmodel
psycopg2-binary
pydantic[email]
pydantic-settings
python-jose[cryptography]
passlib[bcrypt]
```

> **Key change:** Replace `sqlalchemy` + `pydantic` with `sqlmodel` (which bundles both). Add `pydantic-settings` for config management.

#### Step 2 — Configuration (`src/config.py`)
Create centralized settings using `pydantic-settings.BaseSettings`:

```python
# Loads from .env automatically
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://banking_user:banking_pass@localhost:5432/modern_banking"
    JWT_SECRET_KEY: str = "super-secret-change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
```

Also create `server/.env` with the same defaults.

#### Step 3 — Database Core (`src/database/core.py`)
Set up SQLModel engine + session dependency:

```python
from sqlmodel import SQLModel, create_engine, Session
from src.config import get_settings

engine = create_engine(get_settings().DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)  # Auto-creates all tables!

def get_session():
    with Session(engine) as session:
        yield session
```

Call `init_db()` from `main.py` on startup via a **lifespan event**.

---

### Phase 2: Auth System (Steps 4–5)

#### Step 4 — Auth Service (`src/auth/service.py`)
Implement:
- `hash_password(password: str) -> str` — bcrypt hashing via `passlib`
- `verify_password(plain: str, hashed: str) -> bool`
- `create_access_token(data: dict) -> str` — JWT encode with expiry
- `decode_access_token(token: str) -> dict` — JWT decode + validation

#### Step 5 — Auth Controller + Dependencies (`src/auth/controller.py` & `dependencies.py`)

**Controller routes:**
| Method | Endpoint          | Description                    | Auth Required |
|--------|-------------------|--------------------------------|---------------|
| POST   | `/auth/register`  | Register a new user            | ❌            |
| POST   | `/auth/login`     | Login, returns JWT access token| ❌            |

**Dependency (`get_current_user`):**
- Extracts `Bearer` token from `Authorization` header
- Decodes JWT, fetches user from DB
- Returns current `User` object or raises `401`

---

### Phase 3: Entity Models (Step 6)

#### Step 6 — SQLModel Table Definitions

Define all 8 SQLModel tables with proper types, enums, and foreign keys. Each module's `models.py` will contain:

1. **Table model** (SQLModel with `table=True`) — the DB schema
2. **Create schema** (SQLModel) — request body for create
3. **Update schema** (SQLModel) — request body for update (all fields optional)
4. **Read schema** (SQLModel) — response body

**Enum definitions** (shared or inline):
- `KycStatus`: `unverified`, `verified`
- `AccountType`: `savings`, `checking`, `credit_card`, `loan`, `investment`
- `TxnType`: `debit`, `credit`
- `BillStatus`: `upcoming`, `paid`, `overdue`
- `AlertType`: `low_balance`, `bill_due`, `budget_exceeded`

**Example — Users table model:**
```python
class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    password: str
    phone: str
    kyc_status: KycStatus = Field(default=KycStatus.unverified)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

All other tables follow the same pattern with appropriate foreign keys (`user_id`, `account_id`).

---

### Phase 4: CRUD for Every Entity (Steps 7–14)

Each module follows the **same 3-file pattern**: `models.py`, `service.py`, `controller.py`.

#### Service Pattern (Example — Accounts)
```python
class AccountService:
    @staticmethod
    def create(session: Session, user_id: int, data: AccountCreate) -> Account: ...
    
    @staticmethod
    def get_all(session: Session, user_id: int) -> list[Account]: ...
    
    @staticmethod
    def get_by_id(session: Session, account_id: int, user_id: int) -> Account: ...
    
    @staticmethod
    def update(session: Session, account_id: int, user_id: int, data: AccountUpdate) -> Account: ...
    
    @staticmethod
    def delete(session: Session, account_id: int, user_id: int) -> None: ...
```

#### Controller Pattern (Example — Accounts)

| Method    | Endpoint              | Description             | Auth |
|-----------|-----------------------|-------------------------|------|
| POST      | `/accounts`           | Create a new account    | ✅   |
| GET       | `/accounts`           | List user's accounts    | ✅   |
| GET       | `/accounts/{id}`      | Get account by ID       | ✅   |
| PUT       | `/accounts/{id}`      | Update account          | ✅   |
| DELETE    | `/accounts/{id}`      | Delete account          | ✅   |

#### Step-by-step module implementation order:

| Step | Module           | Routes Prefix       | Notes                                                   |
|------|------------------|----------------------|---------------------------------------------------------|
| 7    | **Users**        | `/users`             | Profile CRUD (no create — handled by auth/register)     |
| 8    | **Accounts**     | `/accounts`          | Scoped to `current_user.id`                             |
| 9    | **Transactions** | `/transactions`      | Scoped to user's accounts                               |
| 10   | **Bills**        | `/bills`             | Scoped to `current_user.id`                             |
| 11   | **Rewards**      | `/rewards`           | Scoped to `current_user.id`                             |
| 12   | **Budgets**      | `/budgets`           | Scoped to `current_user.id`                             |
| 13   | **Alerts**       | `/alerts`            | Scoped to `current_user.id`                             |
| 14   | **AdminLogs**    | `/admin-logs`        | Admin-only access                                       |

---

### Phase 5: Wiring & Startup (Step 15)

#### Step 15 — Wire Everything Together

1. **`src/api.py`** — Import and include all module routers:
   ```python
   api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
   api_router.include_router(users_router, prefix="/users", tags=["Users"])
   api_router.include_router(accounts_router, prefix="/accounts", tags=["Accounts"])
   # ... all 8 modules
   ```

2. **`src/main.py`** — Add lifespan for auto table creation + CORS:
   ```python
   @asynccontextmanager
   async def lifespan(app: FastAPI):
       init_db()   # Creates all tables on startup
       yield

   app = FastAPI(title="NeoVault API", lifespan=lifespan)
   app.add_middleware(CORSMiddleware, ...)
   ```

3. **Clean up** — Remove old `todos/` module and `entities/` folder.

---

### Phase 6: Validation & Testing (Step 16)

#### Step 16 — Verify

1. Start the server: `uvicorn src.main:app --reload`
2. Check auto table creation in PostgreSQL
3. Test all endpoints via Swagger UI at `http://localhost:8000/docs`
4. Verify JWT flow: Register → Login → Use token → Access protected routes

---

## 📋 Complete API Endpoints Summary

| #  | Method | Endpoint              | Description                  | Auth |
|----|--------|-----------------------|------------------------------|------|
| 1  | POST   | `/auth/register`      | Register new user            | ❌   |
| 2  | POST   | `/auth/login`         | Login (returns JWT)          | ❌   |
| 3  | GET    | `/users/me`           | Get current user profile     | ✅   |
| 4  | PUT    | `/users/me`           | Update current user profile  | ✅   |
| 5  | DELETE | `/users/me`           | Delete current user          | ✅   |
| 6  | POST   | `/accounts`           | Create account               | ✅   |
| 7  | GET    | `/accounts`           | List user's accounts         | ✅   |
| 8  | GET    | `/accounts/{id}`      | Get account by ID            | ✅   |
| 9  | PUT    | `/accounts/{id}`      | Update account               | ✅   |
| 10 | DELETE | `/accounts/{id}`      | Delete account               | ✅   |
| 11 | POST   | `/transactions`       | Create transaction           | ✅   |
| 12 | GET    | `/transactions`       | List transactions            | ✅   |
| 13 | GET    | `/transactions/{id}`  | Get transaction by ID        | ✅   |
| 14 | PUT    | `/transactions/{id}`  | Update transaction           | ✅   |
| 15 | DELETE | `/transactions/{id}`  | Delete transaction           | ✅   |
| 16 | POST   | `/bills`              | Create bill                  | ✅   |
| 17 | GET    | `/bills`              | List user's bills            | ✅   |
| 18 | GET    | `/bills/{id}`         | Get bill by ID               | ✅   |
| 19 | PUT    | `/bills/{id}`         | Update bill                  | ✅   |
| 20 | DELETE | `/bills/{id}`         | Delete bill                  | ✅   |
| 21 | POST   | `/rewards`            | Create reward                | ✅   |
| 22 | GET    | `/rewards`            | List user's rewards          | ✅   |
| 23 | GET    | `/rewards/{id}`       | Get reward by ID             | ✅   |
| 24 | PUT    | `/rewards/{id}`       | Update reward                | ✅   |
| 25 | DELETE | `/rewards/{id}`       | Delete reward                | ✅   |
| 26 | POST   | `/budgets`            | Create budget                | ✅   |
| 27 | GET    | `/budgets`            | List user's budgets          | ✅   |
| 28 | GET    | `/budgets/{id}`       | Get budget by ID             | ✅   |
| 29 | PUT    | `/budgets/{id}`       | Update budget                | ✅   |
| 30 | DELETE | `/budgets/{id}`       | Delete budget                | ✅   |
| 31 | POST   | `/alerts`             | Create alert                 | ✅   |
| 32 | GET    | `/alerts`             | List user's alerts           | ✅   |
| 33 | GET    | `/alerts/{id}`        | Get alert by ID              | ✅   |
| 34 | PUT    | `/alerts/{id}`        | Update alert                 | ✅   |
| 35 | DELETE | `/alerts/{id}`        | Delete alert                 | ✅   |
| 36 | POST   | `/admin-logs`         | Create admin log             | ✅🔒 |
| 37 | GET    | `/admin-logs`         | List admin logs              | ✅🔒 |
| 38 | GET    | `/admin-logs/{id}`    | Get admin log by ID          | ✅🔒 |
| 39 | PUT    | `/admin-logs/{id}`    | Update admin log             | ✅🔒 |
| 40 | DELETE | `/admin-logs/{id}`    | Delete admin log             | ✅🔒 |
| 41 | GET    | `/health`             | Health check                 | ❌   |

> 🔒 = Admin-only access

---

## ⚡ Key Design Decisions

1. **SQLModel over raw SQLAlchemy** — Single class for both DB model + Pydantic schema, less boilerplate.
2. **Auto table creation** — `SQLModel.metadata.create_all(engine)` on app startup via lifespan.
3. **User scoping** — All queries filter by `current_user.id` to prevent cross-user data access.
4. **JWT via `python-jose`** — Bearer token in Authorization header, decoded via `get_current_user` dependency.
5. **Password hashing** — bcrypt via `passlib` (already in requirements).
6. **Module-per-domain** — Each entity is self-contained with models, service, and controller.
