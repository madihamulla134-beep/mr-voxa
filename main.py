from fastapi import FastAPI

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
  
