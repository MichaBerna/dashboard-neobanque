import pandas as pd
from fastapi import FastAPI
from model.client_data import ClientData
from model.model_loader import load_model
from model.prediction_response import PredictionResponse

app = FastAPI()
model, seuil, preprocessor = load_model()


@app.post("/predict", response_model=PredictionResponse)
async def predict(client_data: ClientData):
    input_data = pd.DataFrame([client_data.model_dump()])
    input_data_processed = preprocessor.transform(input_data)

    probabilite = model.predict_proba(input_data_processed)[0, 1]
    prediction = (probabilite >= seuil).astype(int)

    return PredictionResponse(prediction=prediction, probabilite=probabilite, seuil=seuil)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
