import json
import numpy as np
import pandas
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from schemas.models import AFPModel, InputModel


def calculate_afp(input_data: AFPModel) -> float:

    ilf_weight = 10
    eif_weight = 7
    ei_weight = 4
    eo_weight = 5
    eq_weight = 4

    ufp = (
        input_data.ilf_count * ilf_weight
        + input_data.eif_count * eif_weight
        + input_data.ei_count * ei_weight
        + input_data.eo_count * eo_weight
        + input_data.eq_count * eq_weight
    )

    tcf = sum(input_data.gsc_values)
    afp = ufp * (0.65 + 0.01 * tcf)
    return round(afp)


def predict_duration_and_costs(inputs: InputModel):

    afp = calculate_afp(inputs)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model_file_path = os.path.join(BASE_DIR, "../ml_model/trained-model.pkl")

    loaded_model = joblib.load(model_file_path)

    input_array = pandas.DataFrame(
        [
            [
                afp,
                float(inputs.ei_count),
                float(inputs.eo_count),
                float(inputs.eq_count),
                float(inputs.ilf_count),
                float(inputs.eif_count),
            ]
        ]
    )

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    normalization_file_path = os.path.join(
        BASE_DIR, "../ml_model/normalization_parameters.json"
    )
    
    with open(normalization_file_path, "r") as json_file:
        normalization_parameters = json.load(json_file)

    median = np.array(normalization_parameters["median"])
    scale = np.array(normalization_parameters["scale"])
    input_array = (input_array - median) / scale

    duration = loaded_model.predict(input_array)
    duration = round(abs(duration[0]))
    costs = round(duration * inputs.hourly_pay * inputs.effort, 2)

    return duration, costs, afp