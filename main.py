from fastapi import FastAPI, File, UploadFile
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import io
import torch

app = FastAPI(title="MR Voxa API")

# ASL model location
MODEL_PATH = "../asl_model"

# Load model once when the backend starts
processor = AutoImageProcessor.from_pretrained(MODEL_PATH)
model = AutoModelForImageClassification.from_pretrained(MODEL_PATH)

model.eval()


@app.get("/")
def root():
    return {
        "message": "MR Voxa API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Read uploaded image
    image_bytes = await file.read()

    # Convert image to RGB
    image = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")

    # Prepare image
    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    # Run ASL model
    with torch.no_grad():
        outputs = model(**inputs)

    # Convert model output to probabilities
    probabilities = torch.softmax(
        outputs.logits,
        dim=-1
    )[0]

    # Find highest probability
    predicted_id = probabilities.argmax().item()

    # Get ASL letter
    predicted_label = model.config.id2label[predicted_id]

    # Get confidence
    confidence = probabilities[predicted_id].item()

    return {
        "sign": predicted_label,
        "confidence": confidence
    }
