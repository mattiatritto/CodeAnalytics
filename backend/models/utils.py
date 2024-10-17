import json
import numpy as np
import pandas
import joblib
import os

import pandas

from .models import AFPModel, InputModel


def calculate_afp(input_data: AFPModel) -> float:

    ufp = (
        input_data.ilf_count * input_data.ilf_weight
        + input_data.eif_count * input_data.eif_weight
        + input_data.ei_count * input_data.ei_weight
        + input_data.eo_count * input_data.eo_weight
        + input_data.eq_count * input_data.eq_weight
    )

    tcf = sum(input_data.gsc_values)
    afp = ufp * (0.65 + 0.01 * tcf)
    return afp


def predict_duration_and_costs(inputs: InputModel):

    afp = calculate_afp(inputs)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model_file_path = os.path.join(BASE_DIR, "best_random_forest_model.pkl")

    loaded_model = joblib.load(model_file_path)

    input_array = pandas.DataFrame(
        [
            [
                afp,
                float(inputs.effort),
                float(inputs.ilf_count),
                float(inputs.ei_count),
                float(inputs.eo_count),
                float(inputs.eq_count),
                float(inputs.eif_count),
            ]
        ]
    )

    duration = loaded_model.predict(input_array)
    costs = duration[0] * inputs.hourly_pay

    return duration[0], costs
