"""
Image upload and optimization service.
Handles file uploads, resizing, WebP conversion, and responsive srcset generation.
"""

import asyncio
import io
import uuid
import hashlib
from functools import lru_cache
from pathlib import Path
from typing import Optional
from datetime import datetime
from urllib.parse import urlparse

import boto3
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


def image_to_webp_bytes(image: Image.Image, quality: int = 85) -> bytes:
    """Convert an image to WebP bytes."""
    output = io.BytesIO()
    if image.mode in ("RGBA", "P"):
        image.save(output, "WEBP", quality=quality, method=6)
    else:
        if image.mode != "RGB":
            image = image.convert("RGB")
        image.save(output, "WEBP", quality=quality, method=6)
    return output.getvalue()


def is_r2_enabled() -> bool:
    return settings.UPLOAD_STORAGE == "r2"


def get_r2_endpoint_url() -> str:
    if settings.R2_ENDPOINT_URL:
        return settings.R2_ENDPOINT_URL.rstrip("/")
    return f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com"


@lru_cache(maxsize=1)
def get_r2_client():
    return boto3.client(
        "s3",
        endpoint_url=get_r2_endpoint_url(),
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        region_name="auto",
    )


def build_r2_key(*parts: str) -> str:
    return "/".join(part.strip("/") for part in parts if part.strip("/"))


def build_r2_public_url(key: str) -> str:
    return f"{settings.R2_PUBLIC_URL.rstrip('/')}/{key.lstrip('/')}"


async def upload_r2_object(key: str, content: bytes, content_type: str) -> None:
    client = get_r2_client()
    await asyncio.to_thread(
        client.put_object,
        Bucket=settings.R2_BUCKET_NAME,
        Key=key,
        Body=content,
        ContentType=content_type,
        CacheControl="public, max-age=31536000, immutable",
    )


async def delete_r2_object(key: str) -> bool:
    client = get_r2_client()
    await asyncio.to_thread(
        client.delete_object,
        Bucket=settings.R2_BUCKET_NAME,
        Key=key,
    )
    return True


def extract_r2_key(image_url: str) -> Optional[str]:
    if not image_url:
        return None

    if image_url.startswith("/uploads/"):
        return image_url.lstrip("/")

    public_url = settings.R2_PUBLIC_URL.rstrip("/")
    if public_url and image_url.startswith(f"{public_url}/"):
        return image_url[len(public_url) + 1 :].lstrip("/")

    parsed = urlparse(image_url)
    if parsed.scheme in {"http", "https"} and parsed.netloc == urlparse(public_url).netloc:
        return parsed.path.lstrip("/")

    return None


def extract_upload_relative_path(image_url: str) -> Optional[str]:
    """Extract an uploads-relative path from a relative or absolute image URL."""
    if not image_url:
        return None

    if image_url.startswith("/uploads/"):
        return image_url.replace("/uploads/", "", 1)

    parsed = urlparse(image_url)
    if parsed.scheme in {"http", "https"} and parsed.path.startswith("/uploads/"):
        return parsed.path.replace("/uploads/", "", 1)

    return None


def split_upload_relative_path(relative_path: str) -> tuple[str, str] | None:
    """Return the base upload subfolder and filename from an uploads-relative path."""
    parts = relative_path.split("/")
    if len(parts) < 2:
        return None

    size_names = set(IMAGE_SIZES.keys()) | set(BANNER_SIZES.keys())
    subfolder_parts = parts[:-2] if len(parts) > 2 and parts[-2] in size_names else parts[:-1]
    subfolder = "/".join(subfolder_parts)
    filename = parts[-1]

    if not subfolder or not filename:
        return None

    return subfolder, filename


async def save_upload_to_r2(
    file: UploadFile,
    subfolder: str = "",
    generate_variants: bool = True,
    is_banner: bool = False,
) -> dict:
    validate_image(file)

    content = await file.read()

    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE // (1024*1024)}MB",
        )

    filename = generate_filename(file.filename)
    base_subfolder = validate_subfolder(subfolder or "images")
    original_key = build_r2_key("uploads", base_subfolder, filename)

    await upload_r2_object(
        key=original_key,
        content=content,
        content_type=file.content_type or "application/octet-stream",
    )

    result = {
        "original": build_r2_public_url(original_key),
        "filename": filename,
    }

    if not generate_variants:
        return result

    result["original_size_bytes"] = len(content)

    try:
        image = Image.open(io.BytesIO(content))
    except Exception as e:
        await delete_r2_object(original_key)
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

    webp_content = image_to_webp_bytes(image.copy())
    webp_filename = f"{Path(filename).stem}.webp"
    webp_key = build_r2_key("uploads", base_subfolder, webp_filename)
    await upload_r2_object(webp_key, webp_content, "image/webp")
    result["webp"] = build_r2_public_url(webp_key)
    result["webp_size_bytes"] = len(webp_content)

    sizes = BANNER_SIZES if is_banner else IMAGE_SIZES
    srcset_parts = []

    for size_name, dimensions in sizes.items():
        size_folder = validate_subfolder(f"{base_subfolder}/{size_name}")
        resized = resize_image(image.copy(), dimensions)
        variant_content = image_to_webp_bytes(resized)
        variant_key = build_r2_key("uploads", size_folder, webp_filename)
        await upload_r2_object(variant_key, variant_content, "image/webp")

        variant_url = build_r2_public_url(variant_key)
        result[size_name] = variant_url
        srcset_parts.append(f"{variant_url} {dimensions[0]}w")

    result["srcset"] = ", ".join(srcset_parts)
    if is_banner:
        result["sizes"] = "(max-width: 640px) 640px, (max-width: 1024px) 1024px, 1920px"
    else:
        result["sizes"] = "(max-width: 320px) 320px, (max-width: 640px) 640px, (max-width: 1024px) 1024px, 1920px"

    return result


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
    if is_r2_enabled():
        return await save_upload_to_r2(
            file=file,
            subfolder=subfolder,
            generate_variants=generate_variants,
            is_banner=is_banner,
        )

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
    if is_r2_enabled():
        key = extract_r2_key(image_url)
        if not key or not key.startswith("uploads/"):
            return False

        relative_path = key.replace("uploads/", "", 1)
        split_path = split_upload_relative_path(relative_path)
        if not split_path:
            return False

        subfolder, filename = split_path

        try:
            validate_subfolder(subfolder)
        except HTTPException:
            return False

        base_name = filename.rsplit(".", 1)[0]
        deleted_count = 0

        for size_name in list(IMAGE_SIZES.keys()) + list(BANNER_SIZES.keys()) + [""]:
            for ext in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
                object_key = (
                    build_r2_key("uploads", subfolder, size_name, f"{base_name}{ext}")
                    if size_name
                    else build_r2_key("uploads", subfolder, f"{base_name}{ext}")
                )
                await delete_r2_object(object_key)
                deleted_count += 1

        return deleted_count > 0

    relative_path = extract_upload_relative_path(image_url)
    if not relative_path:
        return False

    split_path = split_upload_relative_path(relative_path)
    if not split_path:
        return False

    subfolder, filename = split_path
    
    # Validate subfolder for security
    try:
        validate_subfolder(subfolder)
    except HTTPException:
        # Invalid subfolder - security check
        return False
    
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
