from fastapi import APIRouter, Form, HTTPException
from app.utils.replicate_client import replicate_client, model_name

router = APIRouter()

@router.post("/fine-tune/")
async def fine_tune(
    training_images_url: str = Form(...),
    trigger_word: str = Form(...),
    steps: int = Form(1000),
    destination_model: str = Form(model_name)  # Use the centralized model name
):
    try:
        training = replicate_client.trainings.create(
            destination=destination_model,
            version="ostris/flux-dev-lora-trainer:e440909d3512c31646ee2e0c7d6f6f4923224863a6a10c494606e79fb5844497",  # Fixed version for training
            input={
                "steps": steps,
                "lora_rank": 16,
                "optimizer": "adamw8bit",
                "batch_size": 1,
                "resolution": "512,768,1024",
                "autocaption": True,
                "input_images": training_images_url,
                "trigger_word": trigger_word,
                "learning_rate": 0.0004,
                "wandb_project": "flux_train_replicate",
                "wandb_save_interval": 100,
                "caption_dropout_rate": 0.05,
                "cache_latents_to_disk": False,
                "wandb_sample_interval": 100,
            },
        )
        return {"training_id": training.id, "status": "Training started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during fine-tuning: {str(e)}")
