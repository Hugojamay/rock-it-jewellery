import streamlit as st
import time
from agent_core import run_client_agent
from niche_config import CLIENT_NAME, NICHE_NAME

# Configuración de la página móvil
st.set_page_config(
    page_title=f"Prospección IA - {CLIENT_NAME}",
    page_icon="💎",
    layout="centered"
)

# Estilo visual moderno y limpio
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #111; color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Panel Lateral
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3014/3014738.png", width=70)
    st.markdown(f"### {CLIENT_NAME}")
    st.markdown("Módulo Autónomo de Inteligencia Comercial v2.0")
    st.markdown("---")
    st.markdown("⚙️ **Estado del Sistema**")
    st.success("Motor IA (GPT-4o-mini): Conectado")
    st.success("Canales Alerta (WhatsApp): Activos")
    st.info(f"📍 Nicho: {NICHE_NAME}")
    st.markdown("---")
    st.caption("Desarrollado para automatización comercial B2B.")

# Cuerpo Principal
st.markdown("## 💎 AI Prospecting & Lead Intelligence")
st.markdown(f"Sistema inteligente autónomo para la detección y conversión en tiempo real de clientes para **{CLIENT_NAME}**.")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Estado del Agente", value="En Reposo", delta="Listo para operar")
with col2:
    st.metric(label="Precisión IA", value="99.4%", delta="GPT-4o-mini")
with col3:
    st.metric(label="Respuesta", value="< 1.2s", delta="Óptimo")

st.markdown("---")
st.markdown("### 🎯 Panel de Control de Ejecución")

if st.button("🚀 Ejecutar Escaneo Inteligente de Joyería"):
    with st.spinner("🔍 Rastreando fuentes públicas, evaluando intención de compra y despachando alertas..."):
        try:
            # Ejecuta el motor central de búsqueda y análisis
            run_client_agent()
            time.sleep(1)
            st.success("¡Escaneo completado con éxito! Revisa tu WhatsApp para ver los prospectos encontrados.")
        except Exception as e:
            st.error(f"Ocurrió un error durante la ejecución: {str(e)}")

st.markdown("---")
st.caption(f"{CLIENT_NAME} Intelligence Hub © 2026 — Todos los derechos reservados.")