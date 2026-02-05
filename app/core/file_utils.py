import os
import uuid
from pathlib import Path
from fastapi import HTTPException, UploadFile
from typing import Optional

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

def validate_image_file(file: UploadFile) -> None:
    # Validate content type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG, PNG, and WEBP are allowed")
    
    # Validate file extension
    if file.filename:
        ext = file.filename.split('.')[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Invalid file extension")
    
    # Validate file size
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size too large. Maximum 2MB allowed")

def save_product_image(file: UploadFile) -> str:
    validate_image_file(file)
    
    # Generate unique filename
    file_ext = file.filename.split('.')[-1].lower() if file.filename else "jpg"
    filename = f"{uuid.uuid4()}.{file_ext}"
    
    # Create upload directory
    upload_dir = Path("uploads/products")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Save file
    file_path = upload_dir / filename
    with open(file_path, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    
    return str(file_path)

def delete_product_image(image_url: Optional[str]) -> None:
    if image_url and os.path.exists(image_url):
        os.remove(image_url)