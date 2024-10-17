import logging
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.exception_handlers import HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from models.models import InputModel
from models.utils import predict_duration_and_costs

app = FastAPI()

# Enable CORS for all origins (adjust as needed)

# Configure logging to a file
logging.basicConfig(
    filename="app.log",
    filemode="a",  # Append mode
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


@app.post("/predict")
async def predict(inputs: InputModel):
    try:
        prediction = predict_duration_and_costs(inputs)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.get("/data")
async def data():
    return FileResponse(
        "./models/dataset.csv", media_type="text/csv", filename="data.csv"
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
