import streamlit as st
import os, glob, datetime, urllib.parse

st.set_page_config(page_title="ARMONTANO PRIVATE CLOUD", page_icon="☁️", layout="wide")

CLAVE = "ARM2027"
CARPETA = "archivos"
os.makedirs(CARPETA, exist_ok=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
* {font-family: Inter, sans-serif}
.top {background:#0f172a;color:white;padding:18px 20px;border-radius:20px;display:flex;justify-content:space-between;align-items:center;margin-bottom:15px}
</style>
""", unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center'>ARMONTANO<br><small style='opacity:.6;letter-spacing:3px;font-size:11px'>PRIVATE CLOUD</small></h1>", unsafe_allow_html=True)
    clave = st.text_input("Clave", type="password", placeholder="Clave")
    if st.button("ACCEDER", use_container_width=True):
        if clave == CLAVE:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Clave incorrecta")
    st.stop()

archivos = [f for f in os.listdir(CARPETA) if os.path.isfile(os.path.join(CARPETA,f))]
hora = datetime.datetime.now().strftime("%H:%M")

st.markdown(f"""
<div class='top'>
<div><h2 style='margin:0;letter-spacing:2px'>ARMONTANO</h2><small style='opacity:.6'>{hora} - {len(archivos)} archivos</small></div>
<small style='background:#10b981;padding:4px 10px;border-radius:20px;font-size:10px'>LIVE ONLINE</small>
</div>
""", unsafe_allow_html=True)

c1,c2,c3 = st.columns(3)
c1.metric("ARCHIVOS", len(archivos))
c2.metric("SEGURO", "100%")
c3.metric("SERVIDOR", "ON")

st.subheader("Subir archivo")
up = st.file_uploader("Elige archivo", label_visibility="collapsed")
if up:
    path = os.path.join(CARPETA, up.name)
    with open(path, "wb") as f:
        f.write(up.getbuffer())
    st.success(f"Subido {up.name}")
    st.rerun()

st.subheader("Mis archivos")
if not archivos:
    st.info("No hay archivos aún.")
else:
    for f in archivos:
        path = os.path.join(CARPETA, f)
        col1, col2 = st.columns([3,1])
        with col1:
            st.write(f"**{f}**")
        with col2:
            with open(path, "rb") as file:
                st.download_button("📥 Descargar", file, file_name=f, key=f"dl_{f}", use_container_width=True)

if st.button("Cerrar sesión"):
    st.session_state.auth = False
    st.rerun()
