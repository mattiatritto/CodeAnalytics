from pydantic import BaseModel, conlist, conint
from datetime import date


class AFPModel(BaseModel):

    ilf_count: conint(ge=0)  # Internal Logical Files (ILF) count
    eif_count: conint(ge=0)  # External Interface Files (EIF) count
    ei_count: conint(ge=0)  # External Inputs (EI) count
    eo_count: conint(ge=0)  # External Outputs (EO) count
    eq_count: conint(ge=0)  # External Inquiries (EQ) count

    # GSC values must be exactly 14 values, each between 0 and 5 (inclusive)
    gsc_values: conlist(conint(ge=0, le=5), min_length=14, max_length=14)
    start_date: date


class InputModel(AFPModel):
    hourly_pay: conint(ge=0)
    num_people: conint(ge=0)
