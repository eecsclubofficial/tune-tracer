from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
from audio import save_audio  
from features import extract
from database import SessionLocal, engine
from models import Feature, Base
from audio_convert import conversion
from pathlib import Path

Base.metadata.create_all(bind = engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"Status" : "Backend Running."}

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    path = await save_audio(file)
    return {"message": "File uploaded", "path": path}

'''
 We are using File(...) as the File upload is necessary and if user does not upload any file,
 automatic error is given to the user, otherwise if we use File(None), user may or may 
 not upload file.
 '''

@app.post("/record")
async def record_audio(file: UploadFile = File(...), db: Session = Depends(get_db)):
    raw_path = await save_audio(file)
    mp3_path = conversion(raw_path)
    features = extract(mp3_path)
    filename = Path(mp3_path).name

    song = Feature(
        rms = float(features[0]),
        tempo = float(features[1]),
        mfcc1 = float(features[2]),
        mfcc2 = float(features[3]),
        mfcc3 = float(features[4]),
        mfcc4 = float(features[5]),
        mfcc5 = float(features[6]),
        mfcc6 = float(features[7]),
        mfcc7 = float(features[8]),
        mfcc8 = float(features[9]),
        mfcc9 = float(features[10]),
        mfcc10 = float(features[11]),
        mfcc11 = float(features[12]),
        mfcc12 = float(features[13]),
        mfcc13 = float(features[14]),
    )
    
    db.add(song)
    db.commit()
    
    return{"Features" : list(features)}


@app.post("/analyse")
async def analyse_audio(file: UploadFile = File(...), db: Session = Depends(get_db)):
    path = await save_audio(file)
    features = extract(path)
    filename = Path(path).name,

    song = Feature(
        rms = float(features[0]),
        tempo = float(features[1]),
        mfcc1 = float(features[2]),
        mfcc2 = float(features[3]),
        mfcc3 = float(features[4]),
        mfcc4 = float(features[5]),
        mfcc5 = float(features[6]),
        mfcc6 = float(features[7]),
        mfcc7 = float(features[8]),
        mfcc8 = float(features[9]),
        mfcc9 = float(features[10]),
        mfcc10 = float(features[11]),
        mfcc11 = float(features[12]),
        mfcc12 = float(features[13]),
        mfcc13 = float(features[14]),
    )

    db.add(song)
    db.commit()

    return{"Features" : list(features)}
    
