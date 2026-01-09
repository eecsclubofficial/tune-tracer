from pydub import AudioSegment
from pathlib import Path

def conversion(input_path: str) -> str:
    input_path = Path(input_path)
    mp3_path = input_path.with_suffix(".mp3")

    audio = AudioSegment.from_file(input_path)
    audio.export(mp3_path, format="mp3")

    return str(mp3_path)