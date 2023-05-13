import streamlit as st
from audio_recorder_streamlit import audio_recorder


def record():
    audio_o = audio_recorder(
        text="Click to Record",
        recording_color="#e8b62c",
        neutral_color="#6aa36f",
        icon_name="user",
        icon_size="2x",
        pause_threshold=3.0
    )
    if audio_o:
        #st.audio(audio_o.tobytes())
        wav_file = open("audio.mp3", "wb")
        wav_file.write(audio_o)
