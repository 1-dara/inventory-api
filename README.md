# 🏪 Inventory Management API

A fully functional retail inventory management backend built with **FastAPI**, **PostgreSQL**, and **JWT authentication**.

## 🚀 Features

- **User Authentication** — Register and login with JWT tokens
- **Role Based Access** — Admin and Staff roles
- **Categories** — Organize products into categories
- **Suppliers** — Track product suppliers
- **Products** — Full CRUD with stock tracking
- **Stock Management** — Track every stock movement in and out
- **Sales Recording** — Auto calculate prices and deduct stock
- **Low Stock Alerts** — Get notified when stock is running low

## 🛠️ Tech Stack

- **Framework** — FastAPI
- **Database** — PostgreSQL
- **ORM** — SQLAlchemy (async)
- **Migrations** — Alembic
- **Authentication** — JWT (python-jose)
- **Password Hashing** — bcrypt (passlib)
- **Validation** — Pydantic

## 🔑 API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login and get JWT token |

### Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories/` | Get all categories |
| POST | `/api/categories/` | Create category (admin only) |
| PUT | `/api/categories/{id}` | Update category (admin only) |
| DELETE | `/api/categories/{id}` | Delete category (admin only) |

### Suppliers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/suppliers/` | Get all suppliers |
| POST | `/api/suppliers/` | Create supplier (admin only) |
| PUT | `/api/suppliers/{id}` | Update supplier (admin only) |
| DELETE | `/api/suppliers/{id}` | Delete supplier (admin only) |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | Get all products with filters |
| GET | `/api/products/low-stock` | Get low stock products |
| POST | `/api/products/` | Create product (admin only) |
| PUT | `/api/products/{id}` | Update product (admin only) |
| DELETE | `/api/products/{id}` | Delete product (admin only) |

### Stock
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stock/{product_id}` | Get stock movements |
| POST | `/api/stock/` | Add stock movement (admin only) |

### Sales
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sales/` | Get all sales |
| POST | `/api/sales/` | Record a sale |

## ⚙️ Setup & Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/inventory-api.git
cd inventory-api
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create a `.env` file**
```env
DATABASE_URL=postgresql+asyncpg://username@localhost:5432/inventory_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. **Run database migrations**
```bash
alembic upgrade head
```

6. **Start the server**
```bash
uvicorn app.main:app --reload
```

7. **Visit the API docs**
```
http://127.0.0.1:8000/docs
``` 