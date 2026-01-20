import joblib
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "ML" / "mood_model.pkl"
ENCODER_PATH = BASE_DIR / "ML" / "label_encoder.pkl"

model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)

FEATURE_COUNT = 6

def predict_mood(features: np.ndarray) -> str:
    if features.shape[1] != FEATURE_COUNT:
        raise ValueError(
            f"Expected {FEATURE_COUNT} features, got {features.shape[1]}"
        )

    prediction_index = model.predict(features)[0]

    try:
        mood = encoder.inverse_transform([prediction_index])[0]
    except Exception:
        mood = str(prediction_index)

    return mood
