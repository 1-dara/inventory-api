from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    staff_id = Column(Integer, ForeignKey(
        "inventory_users.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))

    # Relationships
    product = relationship("Product", back_populates="sales")
    staff = relationship("User", back_populates="sales")
