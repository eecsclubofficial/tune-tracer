import uuid
from fastapi import UploadFile
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

async def save_audio(file: UploadFile) -> str:
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    file_path = UPLOAD_DIR / file_name

    with open (file_path, "wb") as f:
        f.write(await file.read())
    
    return str(file_path)
