from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    low_stock_threshold = Column(Integer, default=10)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(
        timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")
    stock_movements = relationship("Stock", back_populates="product")
    sales = relationship("Sale", back_populates="product")
    images = relationship("ProductImage", back_populates="product")
