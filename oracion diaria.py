import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Meta 365", page_icon="🙏", layout="centered")

# ==============================================================================
# 👇 ZONA DE EDICIÓN: PEGA TUS LINKS AQUÍ 👇
# ==============================================================================

# 1. Pega aquí el enlace que termina en ".csv" (El del Excel publicado)
URL_DATOS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRoKHTOJfvNGvNaTcXZh95b4fiach0dHTAbZ2wDTlbYLhwhgoF0eyscFVn91j-0RzQDkkUijgwXMZG1/pub?output=csv" 

# 2. Pega aquí el enlace del Formulario de Google (El botón 'Enviar' -> Link corto)
URL_FORMULARIO = "https://docs.google.com/forms/d/e/1FAIpQLSdDAQ2_TDjnPtfRR8n26pd_YJ5Cjhd1_lCYQYcMWqPBoRypVw/viewform?usp=header"

# ==============================================================================

def obtener_datos():
    try:
        df = pd.read_csv(URL_DATOS)
        # Forzamos los nombres de columnas para que no fallen
        # Orden esperado: Marca temporal, Participantes, Tema, Frase
        if len(df.columns) >= 3:
            nuevas_columnas = ['FechaHora', 'Participantes', 'Tema']
            # Si hay una 4ta columna (Frase), la agregamos
            if len(df.columns) >= 4:
                nuevas_columnas.append('Frase')
            # Completamos con el resto si sobran columnas
            nuevas_columnas += [f"Col{i}" for i in range(len(nuevas_columnas), len(df.columns))]
            
            df.columns = nuevas_columnas
            df['Fecha'] = pd.to_datetime(df['FechaHora'], dayfirst=True, errors='coerce').dt.date
            return df
        return pd.DataFrame()
    except:
        return pd.DataFrame()

# --- DISEÑO VISUAL ---

st.title("🙏 Meta de Oración 365")
st.write("Nuestro registro de avance espiritual.")

# Botón grande para cargar
st.link_button("📝 REGISTRAR EL DÍA DE HOY", URL_FORMULARIO, type="primary", use_container_width=True)

st.markdown("---")

df = obtener_datos()

if df.empty:
    st.info("⏳ Esperando el primer registro... ¡Estrena la app cargando el día de hoy!")
else:
    # --- 1. BARRA DE PROGRESO ---
    dias_distintos = df['Fecha'].nunique()
    meta = 365
    progreso = min(dias_distintos / meta, 1.0) # Para que no pase del 100%
    
    st.subheader(f"🚀 Avance: Día {dias_distintos} de {meta}")
    st.progress(progreso)
    st.caption(f"Nos faltan {meta - dias_distintos} días para cumplir el año.")

    st.markdown("---")

    # --- 2. EL ÚLTIMO REGISTRO (LO DE HOY) ---
    st.subheader("📖 Última Reunión")
    
    # Tomamos el último dato ingresado
    ultimo = df.iloc[-1]
    
    # Mostramos los datos lindos
    with st.container(border=True):
        st.write(f"**📅 Fecha:** {ultimo['Fecha']}")
        st.write(f"**👥 Participantes:** {ultimo['Participantes']}")
        st.write(f"**🗣️ Tema:** {ultimo['Tema']}")
        
        # Solo mostramos la frase si existe
        if 'Frase' in df.columns and pd.notna(ultimo['Frase']) and str(ultimo['Frase']).strip() != "":

            st.info(f"✨ *\"{ultimo['Frase']}\"*")
