"""
Image upload and optimization service.
Handles file uploads, resizing, WebP conversion, and responsive srcset generation.
"""

import uuid
import hashlib
from pathlib import Path
from typing import Optional
from datetime import datetime

from PIL import Image
from fastapi import UploadFile, HTTPException

from app.core.config import settings


# Image size configurations for responsive images
IMAGE_SIZES = {
    "thumb": (150, 150),      # Thumbnail for lists
    "small": (320, 320),      # Mobile
    "medium": (640, 640),     # Tablet
    "large": (1024, 1024),    # Desktop
    "xlarge": (1920, 1920),   # Full HD
}

# Sizes for banner images (wider aspect ratio)
BANNER_SIZES = {
    "small": (640, 300),
    "medium": (1024, 480),
    "large": (1920, 900),
}

# Allowed subfolders for uploads
ALLOWED_SUBFOLDERS = {"images", "products", "categories", "posts", "brands"}


def validate_subfolder(subfolder: str) -> str:
    """
    Validate and sanitize the upload subfolder.
    
    Prevents path traversal attacks by only allowing whitelisted subfolders.
    Raises HTTPException if subfolder is invalid.
    """
    if not subfolder:
        return "images"  # Default safe subfolder
    
    # Remove any path traversal attempts
    sanitized = subfolder.replace("..", "").replace("\\", "/").strip("/")
    
    # Check if sanitized subfolder is in allowed list
    # Allow subfolders and nested paths like "images/temp" but only with safe base folders
    base_folder = sanitized.split("/")[0]
    
    if not base_folder or base_folder not in ALLOWED_SUBFOLDERS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid subfolder '{subfolder}'. Allowed: {', '.join(ALLOWED_SUBFOLDERS)}"
        )
    
    return sanitized


def validate_image(file: UploadFile) -> None:
    """Validate uploaded file is an allowed image type and size."""
    # Check extension
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{ext}' not allowed. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Check content type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")


def generate_filename(original_filename: str) -> str:
    """Generate a unique filename with timestamp and UUID."""
    ext = original_filename.rsplit(".", 1)[-1].lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    return f"{timestamp}_{unique_id}.{ext}"


def get_safe_path(filename: str, subfolder: str = "") -> Path:
    """
    Get the full path for saving an uploaded file with security checks.
    
    Prevents path traversal attacks by:
    1. Resolving the full path
    2. Verifying it's within the uploads directory
    3. Raising exception if path escapes the uploads directory
    """
    # Validate subfolder
    safe_subfolder = validate_subfolder(subfolder) if subfolder else "images"
    
    # Construct the path
    upload_dir = settings.UPLOAD_DIR.resolve()
    target_dir = (upload_dir / safe_subfolder).resolve()
    target_path = (target_dir / filename).resolve()
    
    # Security check: ensure the target path is within upload directory
    try:
        target_path.relative_to(upload_dir)
    except ValueError:
        # Path is outside upload directory - path traversal attempt
        raise HTTPException(
            status_code=400,
            detail="Invalid file path - potential path traversal attempt"
        )
    
    # Create directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)
    
    return target_path


def get_upload_path(filename: str, subfolder: str = "") -> Path:
    """Get the full path for saving an uploaded file."""
    upload_dir = settings.UPLOAD_DIR / subfolder if subfolder else settings.UPLOAD_DIR
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir / filename


def resize_image(
    image: Image.Image,
    max_size: tuple[int, int],
    maintain_aspect: bool = True
) -> Image.Image:
    """
    Resize image to fit within max_size while maintaining aspect ratio.
    """
    if maintain_aspect:
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        return image
    else:
        return image.resize(max_size, Image.Resampling.LANCZOS)


def convert_to_webp(image: Image.Image, output_path: Path, quality: int = 85) -> Path:
    """Convert image to WebP format and save."""
    webp_path = output_path.with_suffix(".webp")
    
    # Convert RGBA to RGB if necessary (WebP supports both, but smaller with RGB)
    if image.mode in ("RGBA", "P"):
        # Keep alpha for transparency
        image.save(webp_path, "WEBP", quality=quality, method=6)
    else:
        if image.mode != "RGB":
            image = image.convert("RGB")
        image.save(webp_path, "WEBP", quality=quality, method=6)
    
    return webp_path


async def save_upload(
    file: UploadFile,
    subfolder: str = "",
    generate_variants: bool = True,
    is_banner: bool = False
) -> dict:
    """
    Save uploaded image and optionally generate size variants.
    
    Returns a dict with URLs for all generated images:
    {
        "original": "/uploads/image.jpg",
        "webp": "/uploads/image.webp",
        "thumb": "/uploads/thumb/image.webp",
        "small": "/uploads/small/image.webp",
        ...
        "srcset": "url 320w, url 640w, ..."
    }
    """
    validate_image(file)
    
    # Read file content
    content = await file.read()
    
    # Check file size
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE // (1024*1024)}MB"
        )
    
    # Generate unique filename
    filename = generate_filename(file.filename)
    
    # Determine subfolder based on type with safety validation
    base_subfolder = validate_subfolder(subfolder or "images")
    
    # Save original file using secure path
    original_path = get_safe_path(filename, base_subfolder)
    original_path.write_bytes(content)
    
    result = {
        "original": f"/uploads/{base_subfolder}/{filename}",
        "filename": filename,
    }
    
    if not generate_variants:
        return result
    
    result["original_size_bytes"] = len(content)

    # Open image for processing
    try:
        image = Image.open(original_path)
    except Exception as e:
        # Clean up and raise error
        original_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
    
    # Convert original to WebP
    webp_path = convert_to_webp(image.copy(), original_path)
    result["webp"] = f"/uploads/{base_subfolder}/{webp_path.name}"
    result["webp_size_bytes"] = webp_path.stat().st_size
    
    # Generate size variants
    sizes = BANNER_SIZES if is_banner else IMAGE_SIZES
    srcset_parts = []
    
    for size_name, dimensions in sizes.items():
        # Create subfolder for this size with safety validation
        size_folder = f"{base_subfolder}/{size_name}"
        safe_size_folder = validate_subfolder(size_folder)
        
        # Get safe path for variant
        size_path = get_safe_path(filename, safe_size_folder)
        
        # Resize image
        resized = resize_image(image.copy(), dimensions)
        
        # Save as WebP
        webp_variant_path = convert_to_webp(resized, size_path)
        variant_url = f"/uploads/{safe_size_folder}/{webp_variant_path.name}"
        
        result[size_name] = variant_url
        
        # Add to srcset (use width for srcset descriptor)
        width = dimensions[0]
        srcset_parts.append(f"{variant_url} {width}w")
    
    # Build srcset string
    result["srcset"] = ", ".join(srcset_parts)
    
    # Add sizes suggestion
    if is_banner:
        result["sizes"] = "(max-width: 640px) 640px, (max-width: 1024px) 1024px, 1920px"
    else:
        result["sizes"] = "(max-width: 320px) 320px, (max-width: 640px) 640px, (max-width: 1024px) 1024px, 1920px"
    
    return result


async def delete_image(image_url: str) -> bool:
    """
    Delete an image and all its variants.
    
    Uses secure path resolution to prevent path traversal attacks.
    Returns True if deletion was successful.
    """
    if not image_url or not image_url.startswith("/uploads/"):
        return False
    
    # Extract relative path
    relative_path = image_url.replace("/uploads/", "")
    
    # Parse the path components
    parts = relative_path.split("/")
    if len(parts) < 2:
        return False
    
    # First component should be the subfolder
    subfolder = parts[0]
    
    # Validate subfolder for security
    try:
        validate_subfolder(subfolder)
    except HTTPException:
        # Invalid subfolder - security check
        return False
    
    # Get the filename (last component)
    filename = parts[-1]
    
    # Get base filename without extension
    base_name = filename.rsplit(".", 1)[0]
    
    # Construct the safe path for verification
    upload_dir = settings.UPLOAD_DIR.resolve()
    
    deleted_count = 0
    
    # Delete original and variants from all possible locations
    for size_name in list(IMAGE_SIZES.keys()) + list(BANNER_SIZES.keys()) + [""]:
        for ext in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
            try:
                if size_name:
                    check_path = (upload_dir / subfolder / size_name / f"{base_name}{ext}").resolve()
                else:
                    check_path = (upload_dir / subfolder / f"{base_name}{ext}").resolve()
                
                # Security check: ensure path is within upload directory
                check_path.relative_to(upload_dir)
                
                # Safe to delete
                if check_path.exists():
                    check_path.unlink()
                    deleted_count += 1
            except (ValueError, OSError):
                # Path is invalid or outside upload directory - skip
                continue
    
    return deleted_count > 0


def get_image_info(image_url: str) -> Optional[dict]:
    """Get information about an uploaded image."""
    if not image_url or not image_url.startswith("/uploads/"):
        return None
    
    relative_path = image_url.replace("/uploads/", "")
    full_path = settings.UPLOAD_DIR / relative_path
    
    if not full_path.exists():
        return None
    
    try:
        with Image.open(full_path) as img:
            return {
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "mode": img.mode,
                "size_bytes": full_path.stat().st_size,
            }
    except Exception:
        return None
