import streamlit as st
import os
import torch
from TTS.api import TTS
from langdetect import detect
import speech_recognition as sr

# --- 1. PREMIUM VIOLET STYLING ---
st.set_page_config(page_title="Voice Persona Studio", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #2e004f !important; }
    .main-title {
        font-family: 'Trebuchet MS', sans-serif;
        color: #000080 !important;
        text-align: center;
        font-size: 5rem !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 10px #ffffff;
        margin-bottom: 5px;
    }
    .sub-caption {
        text-align: center;
        color: #FFD700 !important;
        font-weight: 600;
        font-size: 1.6rem;
        font-style: italic;
        margin-bottom: 40px;
    }
    .stTextArea textarea {
        background-color: #e3f2fd !important;
        color: #000080 !important;
        border: 4px solid #FFD700 !important; 
        border-radius: 12px;
        font-size: 1.2rem;
    }
    label, h3, p, [data-testid="stMarkdownContainer"] { color: white !important; }
    .instruction-red { border-left: 5px solid #ff4b4b; padding-left: 10px; color: #ff4b4b !important; font-weight: bold; }
    .instruction-blue { border-left: 5px solid #1c83e1; padding-left: 10px; color: #1c83e1 !important; font-weight: bold; }
    div.stButton > button:first-child {
        background-color: #FFD700 !important;
        color: #000080 !important;
        font-weight: bold;
        font-size: 1.4rem !important;
        border-radius: 10px;
        width: 100%;
        height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">VOICE PERSONA STUDIO</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-caption">✨ <i>Precision Multilingual Cloning Engine</i> ✨</p>', unsafe_allow_html=True)

@st.cache_resource
def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return TTS("tts_models/multilingual/multi-dataset/xtts_v2", agree_to_terms=True).to(device)

model = load_model()

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("🎤 Step 1: Capture Voice DNA")
    st.markdown('<p class="instruction-red">🔴 LIVE RECORDING: Speak in English, Hindi, or Telugu.</p>', unsafe_allow_html=True)
    st.markdown('<p class="instruction-blue">🔵 FILE UPLOAD: Drag & drop your MP3/WAV here.</p>', unsafe_allow_html=True)
    input_method = st.radio("Input Method", ["Live Recording", "Upload File"], label_visibility="collapsed")
    
    voice_sample = None
    if input_method == "Live Recording":
        voice_sample = st.audio_input("Record 6-10 seconds")
    else:
        voice_sample = st.file_uploader("Upload audio", type=['mp3', 'wav', 'mpeg', 'm4a'])

with col2:
    st.subheader("📝 Step 2: Input Script")
    text_input = st.text_area("Voice Script", placeholder="Type here... Auto-detection enabled!", height=230)

st.write("---")
if st.button("🚀 GENERATE HIGH-FIDELITY CLONE"):
    if voice_sample and text_input:
        with st.spinner("🧬 Analyzing patterns... please stay with us!"):
            temp_path = "input_sample.wav"
            with open(temp_path, "wb") as f:
                f.write(voice_sample.getbuffer())
            
            try:
                lang = detect(text_input)
                if lang not in ['en', 'hi', 'te']: lang = 'en'
            except:
                lang = 'en'

            model.tts_to_file(text=text_input, speaker_wav=temp_path, language=lang, file_path="output.wav", speed=0.9, temperature=0.82)
            
            st.snow() 
            st.audio("output.wav")
            st.success(f"Generated successfully in {lang.upper()}!")
    else:

        st.error("Please provide both a voice sample and a script.")
