from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

model = joblib.load("mood_model.pkl")
encoder = joblib.load("label_encoder.pkl")

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

    prediction = model.predict(features_array)
    prediction_rounded = int(round(prediction[0]))

    prediction_rounded = max(
        min(prediction_rounded, len(encoder.classes_) - 1),
        0
    )

    mood = encoder.inverse_transform([prediction_rounded])[0]

    return {"predicted_mood": mood}
