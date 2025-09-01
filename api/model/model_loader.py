import os

import joblib

this_dir = os.path.dirname(__file__)


def load_model(model_path=f"{this_dir}/../../modele/modele_prediction_credit.joblib"):
    model_data = joblib.load(model_path)
    return model_data["model"], model_data["seuil"], model_data["preprocessor"]
