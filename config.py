import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Intenta leer primero de Streamlit Secrets (nube), luego de variables de entorno locales (.env)
    OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
    TWILIO_ACCOUNT_SID = st.secrets.get("TWILIO_ACCOUNT_SID", os.getenv("TWILIO_ACCOUNT_SID"))
    TWILIO_AUTH_TOKEN = st.secrets.get("TWILIO_AUTH_TOKEN", os.getenv("TWILIO_AUTH_TOKEN"))
    TWILIO_WHATSAPP_NUMBER = st.secrets.get("TWILIO_WHATSAPP_NUMBER", os.getenv("TWILIO_WHATSAPP_NUMBER"))
    MY_WHATSAPP_NUMBER = st.secrets.get("MY_WHATSAPP_NUMBER", os.getenv("MY_WHATSAPP_NUMBER"))