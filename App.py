import streamlit as st
import requests

# Tu clave queda guardada de forma segura en los Secrets de la nube
CLAVE_API = st.secrets["GEMINI_API_KEY"]

st.set_page_config(page_title="Synápsis Training | Comunicación Benevolente", page_icon="🌿", layout="centered")

# Estilos CSS
st.markdown("""
    <style>
    .stApp { background-color: #F9F9FB; }
    h1 { color: #2D3436 !important; font-family: 'Helvetica Neue', sans-serif; font-size: 1.8rem; text-align: center; }
    .stButton>button { background-color: #2D3436; color: white; border-radius: 8px; border: none; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #4A7C59; color: white; }
    </style>
""", unsafe_allow_html=True)

try:
    st.image("Logotipo.jpeg", width=200)
except:
    st.title("🌿 Synápsis Training")

st.markdown("<h1 style='text-align: center;'>Comunicación Benevolente</h1>", unsafe_allow_html=True)

# Entorno de análisis limpio
contexto = st.selectbox("Selecciona el ámbito:", ["Niños (Formación)", "Jugadores (Rendimiento)", "Padres (Comunicación)", "Directivos (Gestión)"])
mensaje_entrada = st.text_area("Mensaje o situación a analizar:", placeholder="Ej: 'No puedo creer que no hayas hecho caso en el ejercicio...'", height=120)

if 'resultado_generado' not in st.session_state:
    st.session_state.resultado_generado = None

if st.button("Analizar y Reformular"):
    if not mensaje_entrada.strip():
        st.warning("Por favor, escribe el texto a analizar.")
    else:
        prompt = f"""
        Actúa como un facilitador experto de Synápsis Training.
        Analiza este mensaje en el ámbito de '{contexto}': "{mensaje_entrada}"
        
        Aplica la metodología de Comunicación Benevolente adaptada al deporte:
        - Si es con Niños: Prioriza la seguridad psicológica, el refuerzo positivo y la claridad.
        - Si es con Jugadores: Enfoca hacia la autotelia y el rendimiento consciente.
        - Si es con Padres: Busca la alianza educativa y la desescalada.
        - Si es con Directivos: Enfoca hacia la visión y la coherencia institucional.

        Estructura el resultado de forma profesional:
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
        caja_estado.info("⏳ Synápsis analizando conexión neuronal...")
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=45)
            caja_estado.empty()
            if response.status_code == 200:
                data = response.json()
                st.session_state.resultado_generado = data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                st.error("⚠️ Ha ocurrido un error técnico. Por favor, intenta de nuevo en unos segundos.")
        except Exception as e:
            st.error(f"⚠️ Error de conexión: {e}")

if st.session_state.resultado_generado:
    st.markdown(st.session_state.resultado_generado)
    st.download_button(
        label="📥 Descargar Análisis (Markdown)",
        data=st.session_state.resultado_generado,
        file_name="Analisis_Synapsis.md",
        mime="text/markdown"
    )
