import tempfile
import streamlit as st
from .config import get_openai_client

def transcribe_audio(audio_file):
    """音声をWhisperで文字起こし"""
    client = get_openai_client()
    st.info("文字起こし中...")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name
    with open(tmp_path, "rb") as af:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=af
        )
    st.success("文字起こし完了！")
    return transcript.text
