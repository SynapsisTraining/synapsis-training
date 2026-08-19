import streamlit as st
import requests

# Intentamos obtener la clave desde los secretos de la nube
CLAVE_API_NUBE = st.secrets.get("GEMINI_API_KEY", "")

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

with st.sidebar:
    st.header("⚙️ Configuración")
    api_key = st.text_input("API Key:", value=CLAVE_API_NUBE, type="password")
    
    st.subheader("Contexto de Intervención")
    rol = st.selectbox("Tu rol:", ["Entrenador Principal", "Educador Deportivo", "Preparador Físico", "Mentor"])
    interlocutor = st.selectbox("Interlocutor:", ["Niños / Formación", "Jugadores / Rendimiento", "Padres / Familias", "Directivos / Gestión"])

mensaje_entrada = st.text_area("Mensaje o situación a analizar:", placeholder="Ej: 'No puedo creer que no hayas hecho caso en el ejercicio...'", height=120)

if 'resultado_generado' not in st.session_state:
    st.session_state.resultado_generado = None

if st.button("Analizar y Reformular"):
    clave_final = api_key.strip()
    if not clave_final:
        st.error("🔑 Falta incluir la clave API.")
    elif not mensaje_entrada.strip():
        st.warning("Por favor, escribe el texto a analizar.")
    else:
        # Prompt mejorado con los nuevos contextos
        prompt = f"""
        Actúa como un facilitador experto de Synápsis Training.
        Tu usuario es un '{rol}' interactuando con '{interlocutor}'.
        
        Analiza este mensaje: "{mensaje_entrada}"
        
        Aplica la metodología de Comunicación Benevolente adaptada al deporte:
        - Si es con Niños: Prioriza la seguridad psicológica, el refuerzo positivo y la claridad pedagógica.
        - Si es con Jugadores: Enfoca hacia la responsabilidad, la autotelia (motivación intrínseca) y el rendimiento consciente.
        - Si es con Padres: Busca la alianza educativa, la calma y la desescalada de expectativas externas.
        - Si es con Directivos: Enfoca hacia la visión institucional, la coherencia de grupo y los objetivos estratégicos.

        Estructura la respuesta de forma directa y profesional:
        ## 🔍 1. Radiografía de tu Pensamiento (Análisis desde el rol de {rol})
        ## 🌿 2. Reformulación Benevolente Directa (Frase exacta para decir)
        ## 🪞 3. Espejo Emocional (¿Qué necesidad no está cubriendo el interlocutor?)
        ## 🎯 4. Opciones de Estilo (Táctica específica para {interlocutor})
        ## 🎭 5. Simulación del Diálogo (Propuesta de cómo abordar la charla)
        """
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={clave_final}"
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
                st.error(f"⚠️ Error {response.status_code}: Verifica tu clave API.")
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
