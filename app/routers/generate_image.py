from fastapi import APIRouter, Form, HTTPException
from app.utils.replicate_client import replicate_client
import os
import uuid
import requests
import base64

router = APIRouter()

# Endpoint for generating an image
@router.post("/generate-image/")
async def generate_image(
    prompt: str = Form(...),
    seed: int = Form(None),
    model: str = Form("dev"),
    width: int = Form(512, gt=255, lt=1441),
    height: int = Form(512, gt=255, lt=1441),
    extra_lora: str = Form(None),
    lora_scale: float = Form(1, ge=-1, le=2),
    num_outputs: int = Form(1, ge=1, le=4),
    aspect_ratio: str = Form("1:1"),
    output_format: str = Form("webp"),
    guidance_scale: float = Form(3.5, ge=0, le=10),
    output_quality: int = Form(90, ge=0, le=100),
    prompt_strength: float = Form(0.8, ge=0, le=1),
    extra_lora_scale: float = Form(1, ge=-1, le=2),
    num_inference_steps: int = Form(28, ge=1, le=50),
    disable_safety_checker: bool = Form(False)
):
    try:
        # Load model name from environment variable
        model_name = os.getenv("REPLICATE_MODEL_NAME")

        # Fetch the latest version of the model
        model_versions = replicate_client.models.get(model_name).versions.list()
        latest_version = model_versions[0].id if model_versions else ""
        if not latest_version:
            raise ValueError("No version found for the model.")

        # Prepare the input dictionary
        input_data = {
            "prompt": prompt,
            "model": model,
            "width": width,
            "height": height,
            "lora_scale": lora_scale,
            "num_outputs": num_outputs,
            "aspect_ratio": aspect_ratio,
            "output_format": output_format,
            "guidance_scale": guidance_scale,
            "output_quality": output_quality,
            "prompt_strength": prompt_strength,
            "extra_lora_scale": extra_lora_scale,
            "num_inference_steps": num_inference_steps,
            "disable_safety_checker": disable_safety_checker
        }

        # Include optional parameters if provided
        if seed is not None:
            input_data["seed"] = seed

        if extra_lora and (
            extra_lora.startswith("huggingface.co/") or
            extra_lora.startswith("civitai.com/models/") or
            extra_lora.endswith(".safetensors") or
            len(extra_lora.split("/")) in [2, 3]
        ):
            input_data["extra_lora"] = extra_lora

        # Remove keys with None values
        input_data = {k: v for k, v in input_data.items() if v is not None}

        # Use the latest version for image generation
        output = replicate_client.run(
            f"{model_name}:{latest_version}",
            input=input_data
        )

        # Handle the output
        if isinstance(output, list) and output:
            output_item = output[0]
        else:
            output_item = output

        # Generate a unique image path
        image_extension = output_format.lower() if output_format else 'webp'
        image_filename = f"generated_image_{uuid.uuid4().hex}.{image_extension}"
        image_path = os.path.join("generated_images", image_filename)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        try:
            if hasattr(output_item, 'read'):
                # It's a file-like object
                data = output_item.read()
                with open(image_path, "wb") as image_file:
                    image_file.write(data)
            elif isinstance(output_item, str):
                output_url = output_item
                if output_url.startswith("data:"):
                    # Parse and decode the data URL
                    header, encoded = output_url.split(",", 1)
                    data = base64.b64decode(encoded)
                    with open(image_path, "wb") as image_file:
                        image_file.write(data)
                else:
                    # Download the image from the URL
                    response = requests.get(output_url)
                    response.raise_for_status()
                    with open(image_path, "wb") as image_file:
                        image_file.write(response.content)
            else:
                raise ValueError("Unexpected output format from Replicate API.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving the generated image: {str(e)}")

        # Return the URL to access the generated image
        return {"generated_image_url": f"/get-image/{image_filename}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during image generation: {str(e)}")
