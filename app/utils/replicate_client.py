import os
from dotenv import load_dotenv
import replicate

# Load environment variables from .env file
load_dotenv()

# Set the REPLICATE_API_TOKEN from .env
api_token = os.getenv("REPLICATE_API_TOKEN")
if not api_token:
    raise EnvironmentError("REPLICATE_API_TOKEN is not set in the environment.")

# Load model name from .env
model_name = os.getenv("REPLICATE_MODEL_NAME")
if not model_name:
    raise EnvironmentError("Model name is not set in the environment.")

# Initialize the Replicate client
replicate_client = replicate.Client(api_token=api_token)

# Function to retrieve the latest version of the model
def get_latest_model_version():
    model_versions = replicate_client.models.get(model_name).versions.list()
    latest_version = model_versions[0].id if model_versions else ""
    if not latest_version:
        raise ValueError("No version found for the model.")
    return latest_version
