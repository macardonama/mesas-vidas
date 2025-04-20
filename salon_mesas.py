import streamlit as st
import json
import os

ARCHIVO_ESTADO = "estado_mesas.json"
NUM_MESAS = 15
VIDAS_INICIALES = 5

# Inicializar estado
def cargar_estado():
    if os.path.exists(ARCHIVO_ESTADO):
        with open(ARCHIVO_ESTADO, "r") as f:
            return json.load(f)
    else:
        return {str(i): VIDAS_INICIALES for i in range(1, NUM_MESAS + 1)}

def guardar_estado(estado):
    with open(ARCHIVO_ESTADO, "w") as f:
        json.dump(estado, f)

# Restablecer
def reiniciar_estado():
    estado = {str(i): VIDAS_INICIALES for i in range(1, NUM_MESAS + 1)}
    guardar_estado(estado)
    return estado

# Cargar o inicializar
estado_mesas = cargar_estado()

# UI Streamlit
st.set_page_config(page_title="Salón de clases", layout="wide")
st.title("🪑 Sistema de Vidas por Mesa")

# Botón para reiniciar
if st.button("🔄 Reiniciar todas las vidas"):
    estado_mesas = reiniciar_estado()
    st.rerun()

# Dibujar las 15 mesas en 3 filas de 5
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
                    if st.button(f"Quitar vida", key=mesa_num):
                        estado_mesas[mesa_num] = max(vidas - 1, 0)
                        guardar_estado(estado_mesas)
                        st.rerun()
                else:
                    st.markdown("💀 Sin vidas")
