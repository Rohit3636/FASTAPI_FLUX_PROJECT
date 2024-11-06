from fastapi import APIRouter, HTTPException
from app.utils.replicate_client import replicate_client

router = APIRouter()

@router.get("/training-status/{training_id}")
async def training_status(training_id: str):
    try:
        training = replicate_client.trainings.get(training_id)
        return {"status": training.status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching training status: {str(e)}")
