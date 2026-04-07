# 🍽️ SERVORA — Restaurant Order Management API

SERVORA is a production-grade, enterprise-ready RESTful API built to power the complete operational backbone of a modern restaurant ecosystem. 
In today's fast-paced food service industry, seamless digital order management is the difference between a thriving restaurant and an operationally chaotic one. 
SERVORA bridges that gap — delivering a secure, scalable, and cleanly architected backend that handles everything from multi-restaurant registration and role-based access control, to dynamic menu and item management, an in-session cart system, and full order lifecycle tracking. 
With JWT-based authentication, automatic token refresh via middleware, and a layered service-repository architecture, SERVORA is not just a CRUD API — it is a real-world, deployment-ready platform that demonstrates advanced Python backend engineering from the ground up.

---

## 🚀 Tech Stack

| Layer        | Technology                         |
|--------------|------------------------------------|
| Framework    | FastAPI                            |
| Database     | PostgreSQL                         |
| ORM          | SQLAlchemy                         |
| Migrations   | Alembic                            |
| Validation   | Pydantic v2 + pydantic-settings    |
| Auth         | JWT (python-jose) + Passlib/bcrypt |
| Server       | Uvicorn                            |
| DB Driver    | psycopg2-binary                    |
| Package Mgr  | Poetry                             |

---

## 📁 Project Structure

```
SERVORA_restaurent-order-management-api/
├── alembic/                            # Alembic migration setup
│   ├── versions/                       # Auto-generated migration files
│   ├── env.py                          # Alembic environment config
│   ├── README
│   └── script.py.mako                  # Migration script template
├── src/
│   ├── core/
│   │   ├── config.py                   # App settings via pydantic-settings
│   │   └── security.py                 # JWT creation, verification & password hashing
│   ├── database/
│   │   ├── base.py                     # SQLAlchemy declarative Base
│   │   └── session.py                  # DB engine & session factory
│   ├── dependencies/
│   │   └── auth.py                     # JWT bearer extraction & role enforcement
│   ├── exceptions/
│   │   └── custom_exception.py         # Custom service-level exceptions
│   ├── middleware/
│   │   ├── auth_middleware.py          # Token refresh middleware (injects New-Access-Token header)
│   │   └── loggers.py                  # Request/response logging middleware
│   ├── model/
│   │   ├── __init__.py
│   │   ├── user.py                     # User ORM model (USER / ADMIN / RESTAURANT_OWNER roles)
│   │   ├── restaurent.py               # Restaurant ORM model
│   │   ├── menu.py                     # Menu (cuisine category) ORM model
│   │   ├── items.py                    # Menu item ORM model
│   │   ├── order.py                    # Order ORM model
│   │   └── OrderItems.py               # Order-item join table ORM model
│   ├── repository/
│   │   ├── auth.py                     # Auth DB queries
│   │   ├── restaurent.py               # Restaurant DB queries
│   │   ├── order.py                    # Order DB queries
│   │   └── user.py                     # User DB queries
│   ├── routers/
│   │   ├── auth.py                     # Auth routes (signup, login, refresh, make-owner)
│   │   ├── restaurent.py               # Restaurant routes
│   │   ├── menu.py                     # Menu routes
│   │   ├── items.py                    # Item routes
│   │   ├── cart.py                     # Cart routes
│   │   ├── order.py                    # Order routes
│   │   └── user.py                     # User routes
│   ├── schema/
│   │   ├── user.py                     # User Pydantic schemas
│   │   ├── restaurent.py               # Restaurant Pydantic schemas
│   │   ├── menu.py                     # Menu Pydantic schemas
│   │   ├── items.py                    # Item Pydantic schemas
│   │   ├── cart.py                     # Cart Pydantic schemas
│   │   └── order.py                    # Order Pydantic schemas
│   └── service/
│       ├── __init__.py
│       ├── auth.py                     # Auth business logic
│       ├── restaurent.py               # Restaurant business logic
│       ├── menu.py                     # Menu business logic
│       ├── items.py                    # Item business logic
│       ├── cart.py                     # Cart business logic
│       ├── order.py                    # Order business logic
│       └── user.py                     # User business logic
├── main.py                             # App entry point & router registration
├── pyproject.toml                      # Poetry project & dependency config
├── alembic.ini                         # Alembic configuration
├── .env                                # Environment variables (not committed)
└── .gitignore
```

---

## 🔐 Authentication & Roles

SERVORA uses **JWT Bearer token authentication** with automatic token refresh support. Every protected route is guarded by a `require_role()` dependency that enforces role-based access control (RBAC).

### User Roles

| Role                | Permissions                                              |
|---------------------|----------------------------------------------------------|
| `USER`              | Browse menus, manage cart, place and view orders         |
| `RESTAURANT_OWNER`  | Create and manage their own restaurants, menus & items   |
| `ADMIN`             | Full access — all of the above + promote users to owner  |

### Token Flow

- **Access Token** — Short-lived (30 minutes), sent as `Authorization: Bearer <token>`
- **Refresh Token** — Long-lived (1 day), sent in the `Refresh-Token` request header to silently refresh expired sessions
- **Auto-Refresh Middleware** — `TokenRefreshMiddleware` automatically injects a `New-Access-Token` response header when a token is silently refreshed, keeping sessions alive without requiring a re-login

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AmoghShukla/SERVORA_restaurent-order-management-api.git
cd SERVORA_restaurent-order-management-api
```

### 2. Create & Activate a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

Using **Poetry** (recommended):

```bash
pip install poetry
poetry install
```

Or using pip directly:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=servora_db

SECRET_KEY=your_super_secret_key
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

### 5. Create the PostgreSQL Database

Make sure PostgreSQL is running, then create the database:

```sql
CREATE DATABASE servora_db;
```

### 6. Run Database Migrations

```bash
alembic upgrade head
```

### 7. Start the Server

```bash
uvicorn main:app --reload
```

The API will be live at: **http://127.0.0.1:8000**

---

## 📖 API Documentation

FastAPI auto-generates interactive docs:

| UI         | URL                         |
|------------|-----------------------------|
| Swagger UI | http://127.0.0.1:8000/docs  |
| ReDoc      | http://127.0.0.1:8000/redoc |

---

## 🔌 API Endpoints

### Base

| Method | Endpoint | Description                            |
|--------|----------|----------------------------------------|
| GET    | `/`      | Health check — confirms API is running |

---

### 🔑 Auth — `/api/auth`

| Method | Endpoint                               | Auth | Roles | Description                                |
|--------|----------------------------------------|------|-------|--------------------------------------------|
| POST   | `/api/auth/signup`                     | ❌   | —     | Register a new user account                |
| POST   | `/api/auth/login`                      | ❌   | —     | Login and receive access + refresh tokens  |
| POST   | `/api/auth/refresh`                    | ❌   | —     | Exchange refresh token for new access token|
| PATCH  | `/api/auth/users/{user_id}/make-owner` | ✅   | ADMIN | Promote a user to `RESTAURANT_OWNER`       |

---

### 🏪 Restaurants — `/api/restaurent`

| Method | Endpoint            | Auth | Roles                       | Description               |
|--------|---------------------|------|-----------------------------|---------------------------|
| POST   | `/api/restaurent/`  | ✅   | ADMIN, RESTAURANT_OWNER     | Register a new restaurant |

---

### 📋 Menus — `/api/menu`

| Method | Endpoint                    | Auth | Roles                   | Description                    |
|--------|-----------------------------|------|-------------------------|--------------------------------|
| POST   | `/api/menu/{restaurent_id}` | ✅   | ADMIN, RESTAURANT_OWNER | Create a menu for a restaurant |
| GET    | `/api/menu/{restaurent_id}` | ❌   | —                       | Get all menus for a restaurant |

---

### 🍔 Items — `/api/items`

| Method | Endpoint               | Auth | Roles                   | Description              |
|--------|------------------------|------|-------------------------|--------------------------|
| POST   | `/api/items/{menu_id}` | ✅   | ADMIN, RESTAURANT_OWNER | Add a new item to a menu |
| GET    | `/api/items/{menu_id}` | ❌   | —                       | Get all items in a menu  |

---

### 🛒 Cart — `/api/cart`

| Method | Endpoint                                    | Auth | Roles                           | Description                        |
|--------|---------------------------------------------|------|---------------------------------|------------------------------------|
| POST   | `/api/cart/{restaurent_id}/items`           | ✅   | USER, ADMIN, RESTAURANT_OWNER   | Add an item to the cart            |
| GET    | `/api/cart/{restaurent_id}`                 | ✅   | USER, ADMIN, RESTAURANT_OWNER   | View cart for a restaurant         |
| DELETE | `/api/cart/{restaurent_id}/items/{item_id}` | ✅   | USER, ADMIN, RESTAURANT_OWNER   | Remove a specific item from cart   |
| DELETE | `/api/cart/{restaurent_id}`                 | ✅   | USER, ADMIN, RESTAURANT_OWNER   | Clear the entire cart              |

---

### 📦 Orders — `/api/orders`

| Method | Endpoint                | Auth | Roles                         | Description                        |
|--------|-------------------------|------|-------------------------------|------------------------------------|
| POST   | `/api/orders/`          | ✅   | USER, ADMIN, RESTAURANT_OWNER | Place a new order directly         |
| POST   | `/api/orders/from-cart` | ✅   | USER, ADMIN, RESTAURANT_OWNER | Convert current cart into an order |
| GET    | `/api/orders/`          | ✅   | USER, ADMIN, RESTAURANT_OWNER | Get all orders (role-filtered)     |
| GET    | `/api/orders/history`   | ✅   | USER, ADMIN, RESTAURANT_OWNER | Get full order history             |

---

## 🗄️ Database Migrations (Alembic)

| Command                                              | Description                   |
|------------------------------------------------------|-------------------------------|
| `alembic upgrade head`                               | Apply all pending migrations  |
| `alembic revision --autogenerate -m "message"`       | Auto-generate a new migration |
| `alembic downgrade -1`                               | Roll back the last migration  |

---

## 📦 Dependencies

| Package             | Purpose                         |
|---------------------|---------------------------------|
| `fastapi`           | Web framework                   |
| `uvicorn`           | ASGI server                     |
| `sqlalchemy`        | ORM                             |
| `alembic`           | Database migrations             |
| `psycopg2-binary`   | PostgreSQL driver               |
| `pydantic`          | Request/response validation     |
| `pydantic-settings` | Environment config management   |
| `python-jose`       | JWT encoding/decoding           |
| `passlib` + `bcrypt`| Password hashing                |
| `email-validator`   | Email field validation          |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
