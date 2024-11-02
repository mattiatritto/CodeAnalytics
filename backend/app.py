import logging
from io import BytesIO
from datetime import datetime, timedelta
import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.exception_handlers import HTTPException, Request
from schemas.models import InputModel
from utils.utils import predict_duration_and_costs
import requests as req

app = FastAPI()

url = os.getenv("REPORT_SERVICE_URL", "https://report-service-image-771804227712.us-central1.run.app/generate_report/")


# Configure logging to a file
logging.basicConfig(
    filename="logs/app.log",
    filemode="a",  # Append mode
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


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


@app.post("/report")
async def report(inputs: InputModel):
    try:
        prediction = predict_duration_and_costs(inputs)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Calculate the end date
    duration_in_hours = prediction[0]
    workdays = duration_in_hours / 8
    end_date = inputs.start_date + timedelta(days=workdays)

    data = {
        "cost": str(prediction[1]),
        "duration": str(duration_in_hours),
        "afp": str(prediction[2]),
        "start_date": inputs.start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "today_date": datetime.today().strftime("%Y-%m-%d"),
        "ei": str(inputs.ei_count),
        "eq": str(inputs.eq_count),
        "eo": str(inputs.eo_count),
        "ilf": str(inputs.eif_count),
        "eif": str(inputs.eif_count),
    }

    response = req.post(url, json=data)

    if response.status_code == 200:
        output = BytesIO(response.content)
        output.seek(0)
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": "attachment; filename=generated_report.docx"
            },
        )
    else:
        raise HTTPException(
            status_code=response.status_code, detail="Failed to generate report"
        )


@app.get("/data")
async def data():
    return FileResponse("data/dataset.csv", media_type="text/csv", filename="data.csv")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
