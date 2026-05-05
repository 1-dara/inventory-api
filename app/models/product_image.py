from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    image_url = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True),
                         default=lambda: datetime.now(timezone.utc))

    # Relationship back to the Product model
    product = relationship("Product", back_populates="images")
