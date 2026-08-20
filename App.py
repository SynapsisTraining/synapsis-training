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

if 'resultado_generado' not in st.session_state:
    st.session_state.resultado_generado = None

# Formulario limpio y estable
with st.form("formulario_analisis"):
    opciones = ["Personal / Familiar", "Equipo Deportivo", "Comunidad de Vecinos", "Empresa / Equipo de Trabajo", "Centro Educativo / Claustro"]
    contexto = st.selectbox("Selecciona el entorno del conflicto:", opciones)
    mensaje_entrada = st.text_area("Escribe el mensaje o pensamiento a analizar:", placeholder="Ej: 'Estoy harto de que hagas lo que te da la gana...'", height=120)
    
    boton_enviar = st.form_submit_button("Analizar y Reformular")

if boton_enviar:
    if not mensaje_entrada.strip():
        st.warning("Por favor, escribe el texto a analizar.")
    else:
        prompt = f"""
        Actúa como un facilitador experto de Synápsis Training, especializado en Comunicación Benevolente.
        Analiza este texto en el contexto '{contexto}': "{mensaje_entrada}"
        
        IMPORTANTE: Ve directo al grano. Estructura el resultado exactamente con estos encabezados:
        ## 🔍 1. Radiografía de tu Pensamiento
        ## 🌿 2. Reformulación Benevolente Directa
        ## 🪞 3. Espejo Emocional
        ## 🎯 4. Opciones de Estilo
        ## 🎭 5. Simulación del Diálogo
        """
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={CLAVE_API}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4000}
        }
        headers = {"Content-Type": "application/json"}
        
        # Usamos un contenedor de estado limpio para evitar bloqueos en la interfaz
        with st.spinner("⏳ Synápsis procesando conexión neuronal..."):
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=60)
                
                if response.status_code == 200:
                    data = response.json()
                    # Extracción segura de la respuesta
                    try:
                        texto_respuesta = data["candidates"][0]["content"]["parts"][0]["text"]
                        st.session_state.resultado_generado = texto_respuesta
                    except (KeyError, IndexError) as parse_error:
                        st.error(f"⚠️ Error al interpretar la estructura de la respuesta de la IA: {parse_error}")
                        st.write("Datos recibidos:", data)
                else:
                    try:
                        error_data = response.json()
                        error_msg = error_data.get('error', {}).get('message', 'Error desconocido')
                    except:
                        error_msg = response.text
                    st.error(f"⚠️ Error {response.status_code}: {error_msg}")
                    
            except requests.exceptions.Timeout:
                st.error("⚠️ La solicitud ha tardado demasiado tiempo en responder. Inténtalo de nuevo.")
            except Exception as e:
                st.error(f"⚠️ Error de red o conexión: {e}")

# Mostrar el resultado guardado en la sesión de forma totalmente independiente
if st.session_state.resultado_generado:
    st.markdown("---")
    st.markdown(st.session_state.resultado_generado)
    st.download_button(
        label="📥 Descargar Análisis (Markdown)",
        data=st.session_state.resultado_generado,
        file_name="Analisis_Synapsis.md",
        mime="text/markdown"
    )
