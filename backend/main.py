from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
from pathlib import Path
from audio import save_audio
from audio_convert import conversion
from features import extract
from database import SessionLocal, engine
from models import Feature, Base
from ml_model import predict_mood

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"status": "Backend running"}

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    path = await save_audio(file)
    return {"message": "File uploaded", "path": path}

@app.post("/predict")
async def predict_audio(file: UploadFile = File(...)):
    raw_path = await save_audio(file)
    mp3_path = conversion(raw_path)

    features = extract(mp3_path).reshape(1, -1)

    mood = predict_mood(features)

    return {
        "predicted_mood": mood
    }

@app.post("/analyse")
async def analyse_audio(file: UploadFile = File(...)):
    raw_path = await save_audio(file)
    mp3_path = conversion(raw_path)
    features = extract(mp3_path)

    return {
        "features": {
            "mfcc_mean_2": float(features[0]),
            "mfcc_mean_4": float(features[1]),
            "mfcc_mean_7": float(features[2]),
            "zcr_mean": float(features[3]),
            "event_density_mean": float(features[4]),
            "chroma_mean_7": float(features[5]),
        }
    }

@app.post("/record")
async def record_audio(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    raw_path = await save_audio(file)
    mp3_path = conversion(raw_path)
    features = extract(mp3_path)
    filename = Path(mp3_path).name

    song = Feature(
        filename=filename,
        mfcc_mean_2=float(features[0]),
        mfcc_mean_4=float(features[1]),
        mfcc_mean_7=float(features[2]),
        zcr_mean=float(features[3]),
        event_density_mean=float(features[4]),
        chroma_mean_7=float(features[5]),
    )

    db.add(song)
    db.commit()
    db.refresh(song)

    return {
        "message": "Audio processed and stored",
        "id": song.id
    }

