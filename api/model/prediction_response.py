from pydantic import BaseModel


class PredictionResponse(BaseModel):
    prediction: bool
    probabilite: float
    seuil: float
