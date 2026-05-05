from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.product import Product
from app.models.product_image import ProductImage
from app.models.user import User
from app.routers.categories import get_admin_user
from app.core.config import settings
import cloudinary
import cloudinary.uploader

router = APIRouter()

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

# POST endpoint – upload an image for a product


@router.post("/{product_id}/images", status_code=201)
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    # Check if product exists
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(
            status_code=400, detail="Only JPEG, PNG and WebP images are allowed")

    # Read file and upload to Cloudinary
    contents = await file.read()
    upload_result = cloudinary.uploader.upload(
        contents,
        folder=f"inventory/product_{product_id}",
        resource_type="image"
    )
    image_url = upload_result["secure_url"]

    # Save to database
    new_image = ProductImage(
        product_id=product_id,
        image_url=image_url
    )
    db.add(new_image)
    await db.commit()
    await db.refresh(new_image)

    return {"message": "Image uploaded successfully", "image_url": image_url}


# GET endpoint – retrieve all images for a product
@router.get("/{product_id}/images")
async def get_product_images(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ProductImage).where(ProductImage.product_id == product_id)
    )
    return result.scalars().all()
