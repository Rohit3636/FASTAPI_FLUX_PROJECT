from fastapi import FastAPI
from app.routers import fine_tune, generate_image, get_image, training_status

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(fine_tune.router)
app.include_router(generate_image.router)
app.include_router(get_image.router)
app.include_router(training_status.router)
