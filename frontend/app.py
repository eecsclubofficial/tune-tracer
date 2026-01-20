import streamlit as st
import requests
import soundfile as sf
import io
import numpy as np

from streamlit_webrtc import webrtc_streamer, AudioProcessorBase

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Tune-Tracer", layout="centered")
st.title("Tune-Tracer: Music Mood Recognition")

mode = st.radio(
    "Choose audio input method:",
    ("Upload Audio File", "Record from Microphone")
)

def send_audio(file_bytes, filename):
    files = {"file": (filename, file_bytes)}
    return requests.post(f"{BACKEND_URL}/predict", files=files)

if mode == "Upload Audio File":
    uploaded_file = st.file_uploader(
        "Upload an audio file",
        type=["wav", "mp3", "ogg", "flac"]
    )

    if uploaded_file and st.button("Predict Mood"):
        st.audio(uploaded_file)

        with st.spinner("Analyzing audio..."):
            response = send_audio(
                uploaded_file.getvalue(),
                uploaded_file.name
            )

        if response.status_code == 200:
            mood = response.json()["predicted_mood"]
            st.success(f"Predicted Mood: **{mood}**")
        else:
            st.error("Backend error during prediction")

class AudioRecorder(AudioProcessorBase):
    def __init__(self):
        self.frames = []

    def recv_audio(self, frame):
        audio = frame.to_ndarray()
        self.frames.append(audio)
        return frame

if mode == "Record from Microphone":
    st.write("Click **Start**, speak/play music, then click **Stop & Predict**")

    ctx = webrtc_streamer(
        key="mic",
        audio_processor_factory=AudioRecorder,
        media_stream_constraints={"audio": True, "video": False},
    )

    if ctx.audio_processor and st.button("Stop & Predict"):
        if len(ctx.audio_processor.frames) == 0:
            st.error("No audio recorded")
        else:
            audio_np = np.concatenate(ctx.audio_processor.frames, axis=0)

            buffer = io.BytesIO()
            sf.write(buffer, audio_np, samplerate=44100, format="WAV")
            buffer.seek(0)

            with st.spinner("Analyzing audio..."):
                response = send_audio(
                    buffer,
                    "mic_recording.wav"
                )

            if response.status_code == 200:
                mood = response.json()["predicted_mood"]
                st.success(f"Predicted Mood: **{mood}**")
            else:
                st.error("Backend error during prediction")
