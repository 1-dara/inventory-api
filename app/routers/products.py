from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from app.database import get_db
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, LowStockResponse
from app.routers.categories import get_current_user, get_admin_user

router = APIRouter()

# Get all products with optional filters and pagination


@router.get("/", response_model=dict)
async def get_products(
    category_id: Optional[int] = None,
    supplier_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    page: int = 1,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    query = select(Product)

    if category_id is not None:
        query = query.where(Product.category_id == category_id)
    if supplier_id is not None:
        query = query.where(Product.supplier_id == supplier_id)
    if is_active is not None:
        query = query.where(Product.is_active == is_active)

    # Count total results
    count_result = await db.execute(query)
    total = len(count_result.scalars().all())

    # Apply pagination
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    products = result.scalars().all()

    # Convert to list of dicts manually (avoid Pydantic serialization issues)
    products_list = []
    for p in products:
        products_list.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "quantity": p.quantity,
            "low_stock_threshold": p.low_stock_threshold,
            "category_id": p.category_id,
            "supplier_id": p.supplier_id,
            "is_active": p.is_active,
            "created_at": p.created_at.isoformat(),
            "updated_at": p.updated_at.isoformat(),
        })

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
        "products": products_list
    }

# Get low stock products


@router.get("/low-stock", response_model=List[LowStockResponse])
async def get_low_stock_products(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Product))
    products = result.scalars().all()
    low_stock = [p for p in products if p.quantity <= p.low_stock_threshold]
    return low_stock

# Get single product


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

# Create product (admin only)


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    new_product = Product(**product_data.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

# Update product (admin only)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    for field, value in product_data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    await db.commit()
    await db.refresh(product)
    return product

# Delete product (admin only)


@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    await db.delete(product)
    await db.commit()
