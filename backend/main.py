from fastapi import FastAPI, UploadFile, File
from audio import save_audio  

app = FastAPI()

@app.get("/")
def root():
    return {"Status" : "Backend Running."}

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    path = await save_audio(file)
    return {"message": "File uploaded", "path": path}
