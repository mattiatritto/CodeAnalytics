from pydantic import BaseModel
from datetime import date

class ReportData(BaseModel):
    cost: str
    duration: str
    afp: str
    start_date: date
    end_date: date
    today_date: date
    ei: str
    eq: str
    eo: str
    ilf: str
    eif: str