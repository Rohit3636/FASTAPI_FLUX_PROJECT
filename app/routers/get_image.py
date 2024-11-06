from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/get-image/{image_filename}")
async def get_image(image_filename: str):
    image_path = os.path.join("generated_images", image_filename)
    if os.path.exists(image_path):
        return FileResponse(path=image_path, media_type='image/*')
    else:
        raise HTTPException(status_code=404, detail="Image not found")
