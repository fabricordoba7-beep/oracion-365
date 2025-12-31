import streamlit as st
import pandas as pd
import altair as alt # Librería para gráficos lindos

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Meta 365", page_icon="🙏", layout="wide")

# ==============================================================================
# 👇 ZONA DE EDICIÓN: VUELVE A PEGAR TUS LINKS AQUÍ 👇
# ==============================================================================

# 1. Tu enlace CSV del Excel (Publicar en la web)
URL_DATOS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRoKHTOJfvNGvNaTcXZh95b4fiach0dHTAbZ2wDTlbYLhwhgoF0eyscFVn91j-0RzQDkkUijgwXMZG1/pub?output=csv"

# 2. Tu enlace del Formulario (Para el botón)
URL_FORMULARIO = "https://docs.google.com/forms/d/e/1FAIpQLSdDAQ2_TDjnPtfRR8n26pd_YJ5Cjhd1_lCYQYcMWqPBoRypVw/viewform?usp=header"

# ==============================================================================

def obtener_datos():
    try:
        df = pd.read_csv(URL_DATOS)
        # Limpieza y orden de columnas
        if len(df.columns) >= 3:
            # Tomamos las primeras columnas y las renombramos
            # Asumiendo orden: Marca temporal, Participantes, Tema, Frase...
            cols = ['FechaHora', 'Participantes', 'Tema']
            if len(df.columns) >= 4:
                cols.append('Frase')
            
            # Ajustamos el dataframe a esas columnas
            df = df.iloc[:, :len(cols)]
            df.columns = cols
            
            # Convertir fecha
            df['Fecha'] = pd.to_datetime(df['FechaHora'], dayfirst=True, errors='coerce').dt.date
            return df
        return pd.DataFrame()
    except:
        return pd.DataFrame()

# --- INTERFAZ ---

st.title("🙏 Desafío de Oración: Meta 365")
st.markdown("---")

df = obtener_datos()

if df.empty:
    st.info("Esperando datos... Carga el primer día con el botón de abajo.")
else:
    # CÁLCULOS
    dias_orados = df['Fecha'].nunique()
    meta = 365
    falta = meta - dias_orados
    porcentaje = (dias_orados / meta) * 100
    
    # --- ZONA DE GRÁFICOS (Columnas) ---
    col1, col2 = st.columns([1, 2]) # Columna 1 más chica, Columna 2 más grande

    with col1:
        st.subheader("🎯 Meta Anual")
        # Gráfico de DONA (Donut Chart) para el porcentaje
        datos_grafico = pd.DataFrame({
            'Estado': ['Días Orados', 'Días Restantes'],
            'Valor': [dias_orados, falta]
        })
        
        grafico_dona = alt.Chart(datos_grafico).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Valor", type="quantitative"),
            color=alt.Color(field="Estado", type="nominal", 
                          scale=alt.Scale(domain=['Días Orados', 'Días Restantes'],
                                        range=['#4CAF50', '#e0e0e0'])), # Verde y Gris
            tooltip=['Estado', 'Valor']
        )
        st.altair_chart(grafico_dona, use_container_width=True)
        
        # Métrica grande abajo del gráfico
        st.metric("Progreso", f"{porcentaje:.1f}%", f"{dias_orados} días cumplidos")

    with col2:
        st.subheader("📊 Historial de Constancia")
        # Gráfico de BARRAS por fecha
        conteo_diario = df['Fecha'].value_counts().reset_index()
        conteo_diario.columns = ['Fecha', 'Asistencia']
        conteo_diario = conteo_diario.sort_values('Fecha')
        
        st.bar_chart(conteo_diario, x='Fecha', y='Asistencia', color="#4CAF50")
        
        # Tarjeta con el último tema
        ultimo = df.iloc[-1]
        st.info(f"**Último Tema ({ultimo['Fecha']}):** {ultimo['Tema']}")

    st.markdown("---")
    
    # TABLA COMPLETA
    with st.expander("📜 Ver lista completa de oraciones"):
        st.dataframe(df[['Fecha', 'Participantes', 'Tema']], use_container_width=True)

# BOTÓN FLOTANTE FINAL
st.markdown("<br>", unsafe_allow_html=True)
st.link_button("📝 CARGAR DÍA DE HOY", URL_FORMULARIO, type="primary", use_container_width=True)
