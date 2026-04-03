"""
File upload API endpoints.
"""

from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException

from app.api.deps import get_current_user
from app.models import AdminUser
from app.services.image_service import save_upload, delete_image

router = APIRouter()


@router.post("/upload")
async def upload_image(
    current_user: Annotated[AdminUser, Depends(get_current_user)],
    file: UploadFile = File(...),
    subfolder: str = Form(default="images"),
    generate_variants: bool = Form(default=True),
    is_banner: bool = Form(default=False),
):
    """
    Upload an image file.
    
    - **file**: The image file to upload (jpg, jpeg, png, webp, gif)
    - **subfolder**: Subfolder within uploads directory (default: "images")
    - **generate_variants**: Whether to generate resized variants (default: True)
    - **is_banner**: Whether this is a banner image (uses wider aspect ratios)
    
    Returns URLs for the original image and all generated variants.
    """
    result = await save_upload(
        file=file,
        subfolder=subfolder,
        generate_variants=generate_variants,
        is_banner=is_banner,
    )
    
    return {
        "success": True,
        "data": result,
    }


@router.post("/upload/multiple")
async def upload_multiple_images(
    current_user: Annotated[AdminUser, Depends(get_current_user)],
    files: list[UploadFile] = File(...),
    subfolder: str = Form(default="images"),
    generate_variants: bool = Form(default=True),
    is_banner: bool = Form(default=False),
):
    """
    Upload multiple image files.
    
    Returns URLs for all uploaded images and their variants.
    """
    results = []
    errors = []
    
    for file in files:
        try:
            result = await save_upload(
                file=file,
                subfolder=subfolder,
                generate_variants=generate_variants,
                is_banner=is_banner,
            )
            results.append(result)
        except HTTPException as e:
            errors.append({
                "filename": file.filename,
                "error": e.detail,
            })
        except Exception as e:
            errors.append({
                "filename": file.filename,
                "error": str(e),
            })
    
    return {
        "success": len(errors) == 0,
        "data": results,
        "errors": errors if errors else None,
    }


@router.delete("/upload")
async def remove_image(
    current_user: Annotated[AdminUser, Depends(get_current_user)],
    image_url: str,
):
    """
    Delete an uploaded image and all its variants.
    
    - **image_url**: The URL of the image to delete (e.g., "/uploads/images/file.webp")
    """
    success = await delete_image(image_url)
    
    if not success:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return {
        "success": True,
        "message": "Image deleted successfully",
    }
