from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database import get_db
from app.models.sale import Sale
from app.models.product import Product
from app.models.stock import Stock
from app.models.user import User
from app.schemas.sale import SaleCreate, SaleResponse
from app.routers.categories import get_current_user

router = APIRouter()

# Get all sales


@router.get("/", response_model=List[SaleResponse])
async def get_sales(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Sale))
    return result.scalars().all()

# Record a sale


@router.post("/", response_model=SaleResponse, status_code=201)
async def create_sale(
    sale_data: SaleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check product exists
    result = await db.execute(select(Product).where(Product.id == sale_data.product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # Check product is active
    if not product.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product is not active"
        )

    # Check enough stock
    if product.quantity < sale_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not enough stock! Available: {product.quantity}"
        )

    # Calculate prices
    unit_price = product.price
    total_price = unit_price * sale_data.quantity

    # Deduct stock from product
    product.quantity -= sale_data.quantity

    # Record stock movement
    stock_movement = Stock(
        product_id=product.id,
        movement_type="out",
        quantity=sale_data.quantity,
        reason="sale"
    )

    # Create the sale
    new_sale = Sale(
        product_id=sale_data.product_id,
        staff_id=current_user.id,
        quantity=sale_data.quantity,
        unit_price=unit_price,
        total_price=total_price
    )

    db.add(stock_movement)
    db.add(new_sale)
    await db.commit()
    await db.refresh(new_sale)
    return new_sale
