from fastapi import FastAPI
from app.routers import auth, categories, products, suppliers, stock, sales, product_images

app = FastAPI(
    title="Inventory Management API",
    description="Backend for a retail inventory management system",
    version="1.0.0"
)

# Register all routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(categories.router,
                   prefix="/api/categories", tags=["Categories"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(
    suppliers.router, prefix="/api/suppliers", tags=["Suppliers"])
app.include_router(stock.router, prefix="/api/stock", tags=["Stock"])
app.include_router(sales.router, prefix="/api/sales", tags=["Sales"])
app.include_router(product_images.router,
                   prefix="/api/products", tags=["Product Images"])


@app.get("/")
async def root():
    return {"message": "Inventory Management API is running 🏪"}
