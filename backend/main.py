from fastapi import FastAPI, UploadFile, File
from audio import save_audio  
from features import extract
from database import SessionLocal
from models import SongFeature

app = FastAPI()

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

@app.post("/analyse")
async def analyse_audio(file: UploadFile = File(...)):
    path = await save_audio(file)
    features = extract(path)

    db = SessionLocal()

    song = SongFeature(
        filename = file.filename,
        rms = features[0],
        tempo = features[1],
        mfcc1=features[2], 
        mfcc2=features[3], 
        mfcc3=features[4], 
        mfcc4=features[5], 
        mfcc5=features[6], 
        mfcc6=features[7], 
        mfcc7=features[8], 
        mfcc8=features[9], 
        mfcc9=features[10], 
        mfcc10=features[11], 
        mfcc11=features[12], 
        mfcc12=features[13], 
        mfcc13=features[14]
    )

    db.add(song)
    db.commit()
    db.close()

    return{"Features" : list(features)}
    
