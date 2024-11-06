# FASTAPI_FLUX_PROJECT

A FastAPI-based application for fine-tuning and generating images using Replicate's machine learning models. The project allows users to fine-tune models with custom datasets, generate images based on prompts, retrieve generated images, and check the status of training processes.

## Table of Contents
- Project Structure
- Setup Instructions
- Interacting with the Application
  1. CURL Requests
  2. Swagger UI
- Endpoints Overview
  1. Fine-tune Model (POST /fine-tune/)
  2. Generate Image (POST /generate-image/)
  3. Get Generated Image (GET /get-image/{image_filename})
  4. Training Status (GET /training-status/{training_id})
- Utilities
- Directory Descriptions

## Project Structure
```bash
FASTAPI_FLUX_PROJECT/
├── .env                        # Environment variables file (No changes needed here).
├── app/                        # Application package (Core application logic resides here).
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point.
│   ├── routers/                # FastAPI routers for handling different API endpoints.
│   │   ├── __init__.py
│   │   ├── fine_tune.py        # API to fine-tune models with a custom dataset.
│   │   ├── generate_image.py   # API to generate images using a fine-tuned model.
│   │   ├── get_image.py        # API to retrieve generated images.
│   │   └── training_status.py  # API to check the status of an ongoing training.
│   └── utils/
│       ├── __init__.py
│       └── replicate_client.py # Utility for handling Replicate API communication.
├── generated_images/           # Folder for storing generated images.
│   └── <generated_images_here>.webp
├── training_images/            # Folder for training image datasets (uploaded externally - https://tmpfiles.org/).
│   └── pic14.zip               # Zip file containing training data.
├── requirements.txt            # List of project dependencies (No changes needed).
└── README.md                   # Project documentation (You're currently reading this).
```

## Setup Instructions

1. **Install dependencies**: Ensure Python 3.8+ is installed. Run the following command to install all required libraries:

```bash
   pip install -r requirements.txt
```

2. **Configure Environment Variables**: The `.env` file contains essential API tokens and model IDs. No changes are required unless you're working with different models or API tokens.

   - `REPLICATE_API_TOKEN`: The token required to access the Replicate API.
   - `REPLICATE_MODEL_NAME`: The name of the model to be used in the Replicate API (default: `rohit3636/newtraining`).

3. **Running the Application**: To start the FastAPI application, run the following command:

```bash
   uvicorn app.main:app --reload
```

   The API will be accessible at [http://localhost:8000](http://localhost:8000).

## Interacting with the Application

There are two ways to interact with the FastAPI application:

### 1. CURL Requests

You can interact with the API by sending CURL requests. This method is useful for scripting or using command-line tools to test the API endpoints.

**Example CURL request**:

```bash
curl -X POST "http://localhost:8000/generate-image/" \
-F "prompt=an anime character in a futuristic city" \
-F "width=512" \
-F "height=512" \
-F "num_outputs=2" \
-F "output_format=webp"
```

### 2. Swagger UI

FastAPI automatically generates a web-based UI (Swagger UI) for interacting with the API without the need for external tools. You can visit the `/docs` endpoint after starting the application to interact with all available endpoints, view request/response structures, and test API features directly in your browser.

**URL**: [http://localhost:8000/docs](http://localhost:8000/docs)

The Swagger UI offers a user-friendly way to explore and test the API without writing code. All available endpoints are documented, and you can easily send requests by filling in the required fields and parameters directly from the interface.

## Endpoints Overview

### 1. Fine-tune Model (POST /fine-tune/)

This endpoint allows users to fine-tune a model with a custom dataset. The model will be trained using the provided dataset and hyperparameters. The dataset must be uploaded as a ZIP file to an external service (e.g., https://tmpfiles.org/) and then passed as a URL in the request.

- **Endpoint**: `/fine-tune/`
- **Method**: POST
- **Parameters**:
  - `training_images_url` (required, str): The URL to the ZIP file containing training images.
  - `trigger_word` (required, str): A word or phrase to associate with the model's training.
  - `steps` (optional, int): The number of training steps (default: 1000).
  - `destination_model` (optional, str): The name of the destination model to save the fine-tuned version.

**Example Request**:

```bash
curl -X POST "http://localhost:8000/fine-tune/" \
-F "training_images_url=https://tmpfiles.org/dl/xyz123/pic14.zip" \
-F "trigger_word=mytrigger" \
-F "steps=1000" \
-F "destination_model=my_new_model"
```

**Response**:

```json
{
  "training_id": "xyz456",
  "status": "Training started"
}
```

### 2. Generate Image (POST /generate-image/)

This endpoint generates an image based on a text prompt and other optional parameters. The model version is fetched dynamically from the Replicate API, and images can be customized using various hyperparameters.

- **Endpoint**: `/generate-image/`
- **Method**: POST
- **Parameters**:
  - `prompt` (required, str): The text prompt for generating the image.
  - `seed` (optional, int): The seed for random number generation to ensure consistent outputs.
  - `model` (optional, str): The model identifier (default: `dev`).
  - `width` (optional, int): The width of the generated image (default: 512, min: 256, max: 1440).
  - `height` (optional, int): The height of the generated image (default: 512, min: 256, max: 1440).
  - `extra_lora` (optional, str): Path to additional LoRA model if needed.
  - `lora_scale` (optional, float): Scaling factor for LoRA layers (default: 1, range: -1 to 2).
  - `num_outputs` (optional, int): Number of images to generate (default: 1, max: 4).
  - `output_format` (optional, str): Output image format (default: `webp`).
  - `guidance_scale` (optional, float): How closely the image should follow the prompt (default: 3.5).
  - `num_inference_steps` (optional, int): Number of inference steps for image generation (default: 28).
  - `disable_safety_checker` (optional, bool): Disable safety checks (default: `false`).

**Example Request**:

```bash
curl -X POST "http://localhost:8000/generate-image/" \
-F "prompt=an anime character in a futuristic city" \
-F "width=512" \
-F "height=512" \
-F "num_outputs=2" \
-F "output_format=webp"
```

**Response**:

```json
{
  "generated_image_url": "/get-image/generated_image_abc123.webp"
}
```

### 3. Get Generated Image (GET /get-image/{image_filename})

This endpoint retrieves an image that was previously generated by the model. The images are stored in the `generated_images/` folder.

- **Endpoint**: `/get-image/{image_filename}`
- **Method**: GET
- **Parameters**:
  - `image_filename` (required, str): The filename of the generated image.

**Example Request**:

```bash
GET "http://localhost:8000/get-image/generated_image_abc123.webp"
```

**Response**: The image file will be served as the response.

### 4. Training Status (GET /training-status/{training_id})

This endpoint allows users to check the status of a model training process using a unique `training_id` provided during the fine-tuning phase.

- **Endpoint**: `/training-status/{training_id}`
- **Method**: GET
- **Parameters**:
  - `training_id` (required, str): The ID of the ongoing training process.

**Example Request**:

```bash
GET "http://localhost:8000/training-status/xyz456"
```

**Response**:

```json
{
  "status": "In progress"
}
```

## Utilities

- `replicate_client.py`: A utility module responsible for communicating with the Replicate API. It includes functionality to create fine-tuning tasks, retrieve model versions, and generate images.

## Directory Descriptions

- `generated_images/`: This folder stores all generated images by the model. Each image is stored with a unique filename generated at runtime.

- `training_images/`: This folder stores images that are used for training the model. However, in this implementation, we upload the training images externally to services like https://tmpfiles.org/ and pass the URL in the fine-tuning API request.
