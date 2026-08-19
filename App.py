import streamlit as st
import requests

# Tu clave se lee de forma segura desde los Secrets de Streamlit Cloud
CLAVE_API = st.secrets["GEMINI_API_KEY"]

st.set_page_config(page_title="Synápsis Training | Comunicación Benevolente", page_icon="🌿", layout="centered")

# Estilos CSS
st.markdown("""
    <style>
    .stApp { background-color: #F9F9FB; }
    h1 { color: #2D3436 !important; font-family: 'Helvetica Neue', sans-serif; font-size: 2rem; text-align: center; }
    .stButton>button { background-color: #2D3436; color: white; border-radius: 8px; border: none; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #4A7C59; color: white; }
    </style>
""", unsafe_allow_html=True)

try:
    st.image("Logotipo.jpeg", width=250)
except:
    st.title("🌿 Synápsis Training")

st.markdown("<h1 style='text-align: center;'>Comunicación Benevolente</h1>", unsafe_allow_html=True)

# Tus entornos originales
contexto = st.selectbox("Selecciona el entorno del conflicto:", ["Comunidad de Vecinos", "Empresa / Equipo de Trabajo", "Centro Educativo / Claustro", "Personal / Familiar"])
mensaje_entrada = st.text_area("Escribe el mensaje o pensamiento a analizar:", placeholder="Ej: 'Estoy harto de que hagas lo que te da la gana...'", height=120)

if 'resultado_generado' not in st.session_state:
    st.session_state.resultado_generado = None

if st.button("Analizar y Reformular"):
    if not mensaje_entrada.strip():
        st.warning("Por favor, escribe el texto a analizar.")
    else:
        prompt = f"""
        Actúa como un facilitador experto de Synápsis Training, especializado en Comunicación Benevolente.
        Analiza este texto en el contexto '{contexto}': "{mensaje_entrada}"
        
        IMPORTANTE: Ve directo al grano. Estructura el resultado con estos encabezados:
        ## 🔍 1. Radiografía de tu Pensamiento
        ## 🌿 2. Reformulación Benevolente Directa
        ## 🪞 3. Espejo Emocional
        ## 🎯 4. Opciones de Estilo
        ## 🎭 5. Simulación del Diálogo
        """
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={CLAVE_API}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4000}
        }
        headers = {"Content-Type": "application/json"}
        
        caja_estado = st.empty()
        caja_estado.info("⏳ Synápsis procesando conexión neuronal...")
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=45)
            caja_estado.empty()
            if response.status_code == 200:
                data = response.json()
                st.session_state.resultado_generado = data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                error_msg = response.json().get('error', {}).get('message', 'Error desconocido')
                st.error(f"⚠️ Error {response.status_code}: {error_msg}")
        except Exception as e:
            st.error(f"⚠️ Error de red: {e}")

if st.session_state.resultado_generado:
    st.markdown(st.session_state.resultado_generado)
    st.download_button(
        label="📥 Descargar Análisis (Markdown)",
        data=st.session_state.resultado_generado,
        file_name="Analisis_Synapsis.md",
        mime="text/markdown"
    )
