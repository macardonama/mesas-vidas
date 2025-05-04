
import streamlit as st
import json
import os
from datetime import datetime

ARCHIVO_ESTADO = "estado_mesas.json"
NUM_MESAS = 15
VIDAS_INICIALES = 5

def cargar_estado():
    if os.path.exists(ARCHIVO_ESTADO):
        with open(ARCHIVO_ESTADO, "r") as f:
            return json.load(f)
    else:
        return {str(i): VIDAS_INICIALES for i in range(1, NUM_MESAS + 1)}

def guardar_estado(estado):
    with open(ARCHIVO_ESTADO, "w") as f:
        json.dump(estado, f)

def reiniciar_estado():
    estado = {str(i): VIDAS_INICIALES for i in range(1, NUM_MESAS + 1)}
    guardar_estado(estado)
    return estado

estado_mesas = cargar_estado()

st.set_page_config(page_title="Salón de clases", layout="wide")
st.title("🪑 Sistema de Vidas por Mesa")

st.markdown("## 🕒 Hora actual: " + datetime.now().strftime("%H:%M:%S"))

if "semaforo" not in st.session_state:
    st.session_state["semaforo"] = True

if st.button("🟢 Encendido" if st.session_state["semaforo"] else "🔴 Apagado"):
    st.session_state["semaforo"] = not st.session_state["semaforo"]
    st.rerun()

if st.button("🔄 Reiniciar todas las vidas"):
    estado_mesas = reiniciar_estado()
    st.rerun()

for fila in range(3):
    cols = st.columns(5)
    for i in range(5):
        mesa_num = str(fila * 5 + i + 1)
        if mesa_num in estado_mesas:
            vidas = estado_mesas[mesa_num]
            with cols[i]:
                st.markdown(f"### Mesa {mesa_num}")
                if vidas > 0:
                    st.markdown("❤️ " * vidas)
                else:
                    st.markdown("💀 Sin vidas")
                col1, col2 = st.columns(2)
                with col1:
                    if vidas > 0 and st.button("➖ Quitar vida", key=f"quitar_{mesa_num}"):
                        estado_mesas[mesa_num] = max(vidas - 1, 0)
                        guardar_estado(estado_mesas)
                        st.rerun()
                with col2:
                    if vidas < VIDAS_INICIALES and st.button("➕ Recargar vida", key=f"recargar_{mesa_num}"):
                        estado_mesas[mesa_num] = min(vidas + 1, VIDAS_INICIALES)
                        guardar_estado(estado_mesas)
                        st.rerun()
