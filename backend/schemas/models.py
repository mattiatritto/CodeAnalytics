from pydantic import BaseModel, conlist, conint
from datetime import date


class AFPModel(BaseModel):

    ilf_count: conint(ge=0)
    eif_count: conint(ge=0)
    ei_count: conint(ge=0)
    eo_count: conint(ge=0)
    eq_count: conint(ge=0)

    gsc_values: conlist(conint(ge=0, le=5), min_length=14, max_length=14)
    start_date: date


class InputModel(AFPModel):
    hourly_pay: conint(ge=0)
    num_people: conint(ge=0)
