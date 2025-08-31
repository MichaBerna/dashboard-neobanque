import joblib


def load_model(model_path="../modele/modele_prediction_credit.joblib"):
    model_data = joblib.load(model_path)
    return model_data["model"], model_data["seuil"], model_data["preprocessor"]
