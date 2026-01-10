from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()
import os
model_path = os.path.join("ML", "mood_model.pkl")
encoder_path = os.path.join("ML", "label_encoder.pkl")

model = joblib.load(model_path)
encoder = joblib.load(encoder_path)

FEATURE_COUNT = 13


class PredictionRequest(BaseModel):
    features: list[float]


@app.get("/")
def home():
    return {"message": "Tune-Tracer ML API is running"}


@app.post("/predict")
def predict(
    request: PredictionRequest = Body(..., media_type="application/json")
):
    if len(request.features) != FEATURE_COUNT:
        raise HTTPException(
            status_code=422,
            detail=f"Expected {FEATURE_COUNT} features, got {len(request.features)}"
        )
    features_array = np.array(request.features).reshape(1, -1)

    prediction_index = model.predict(features_array)[0]

    try:
        mood = encoder.inverse_transform([prediction_index])[0]
    except ValueError:
        mood = str(prediction_index)

    return {"predicted_mood": mood}