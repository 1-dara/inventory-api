#  Inventory Management API

A fully functional, production-grade retail inventory management backend built with **FastAPI** and **PostgreSQL**. Deployed and live.

 **Live API Docs:** https://inventory-api-vd7f.onrender.com/docs   
 **GitHub:** https://github.com/1-dara/inventory-api

---

##  Features

- **JWT Authentication** — Secure register and login with access tokens
- **Role-Based Access Control** — Admin and Staff role separation
- **Product Management** — Full CRUD with category and supplier linking
- **Stock Tracking** — Complete audit trail of every stock movement (in/out)
- **Low Stock Alerts** — Automatic alerts when products fall below threshold
- **Sales Recording** — Auto price calculation and stock deduction on sale
- **Price Snapshotting** — Historical price accuracy on all sales records
- **Supplier Management** — Track who supplies each product
- **Category Management** — Organize products into categories
- **Auto-generated Docs** — Interactive Swagger UI at `/docs`

---

##  Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Web framework |
| PostgreSQL | Database |
| SQLAlchemy (Async) | ORM |
| Alembic | Database migrations |
| JWT / OAuth2 | Authentication |
| bcrypt | Password hashing |
| Render | Deployment |
| Pydantic | Data validation |

---

##  API Endpoints

### Auth
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/auth/register` | Register a new user | ❌ |
| POST | `/api/auth/login` | Login and get JWT token | ❌ |

### Products
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/products/` | Get all products with filters | ❌ |
| GET | `/api/products/low-stock` | Get low stock products | ✅ |
| POST | `/api/products/` | Create a product | ✅ Admin only |
| PUT | `/api/products/{id}` | Update a product | ✅ Admin only |
| DELETE | `/api/products/{id}` | Delete a product | ✅ Admin only |

### Stock
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/stock/{product_id}` | Get stock movements | ✅ |
| POST | `/api/stock/` | Add stock movement | ✅ Admin only |

### Sales
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/sales/` | Get all sales | ✅ |
| POST | `/api/sales/` | Record a sale | ✅ |

---

##  Setup & Installation

1. **Clone the repository**
```bash
git clone https://github.com/1-dara/inventory-api.git
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

---

##  Author

**Irene Peter-Okon Idara**  
Backend Engineer  
 1ireneokon@gmail.com  
 github.com/1-dara
