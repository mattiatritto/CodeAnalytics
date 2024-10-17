from pydantic import BaseModel, conlist, conint


class AFPModel(BaseModel):

    ilf_count: conint(ge=0)  # Internal Logical Files (ILF) count
    eif_count: conint(ge=0)  # External Interface Files (EIF) count
    ei_count: conint(ge=0)  # External Inputs (EI) count
    eo_count: conint(ge=0)  # External Outputs (EO) count
    eq_count: conint(ge=0)  # External Inquiries (EQ) count

    # Weight fields with range 1 to 10
    ilf_weight: conint(ge=1, le=10)
    eif_weight: conint(ge=1, le=10)
    ei_weight: conint(ge=1, le=10)
    eo_weight: conint(ge=1, le=10)
    eq_weight: conint(ge=1, le=10)

    # GSC values must be exactly 14 values, each between 0 and 5 (inclusive)
    gsc_values: conlist(conint(ge=0, le=5), min_length=14, max_length=14)


class InputModel(AFPModel):
    hourly_pay: conint(ge=0)
    effort: conint(ge=0)
