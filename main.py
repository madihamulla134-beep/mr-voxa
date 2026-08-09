from fastapi import FastAPI, File, UploadFile

app = FastAPI(title="MR Voxa API")


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
    return {
        "message": "Image received successfully",
        "filename": file.filename
    }
