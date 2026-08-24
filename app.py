import json
import os
import re
from html import escape

import requests
import streamlit as st


st.set_page_config(
    page_title="Brújula 36 | Discernimiento consciente",
    page_icon="✦",
    layout="centered",
)

st.markdown(
    """
    <style>
    :root { --ink:#25332f; --sage:#5f786c; --mist:#eef3ef; --gold:#b59055; }
    .stApp { background: linear-gradient(180deg,#f8faf8 0%,#f4f1eb 100%); color:var(--ink); }
    .block-container { max-width:850px; padding-top:2.2rem; }
    h1,h2,h3 { color:var(--ink) !important; letter-spacing:-0.02em; }
    .hero { padding:1.4rem 1.5rem; border:1px solid #dce5de; border-radius:22px;
            background:rgba(255,255,255,.82); box-shadow:0 8px 30px rgba(53,75,65,.07); }
    .eyebrow { color:var(--gold); text-transform:uppercase; font-size:.78rem;
               letter-spacing:.14em; font-weight:700; }
    .subtitle { color:#586760; font-size:1.05rem; line-height:1.6; margin-bottom:.2rem; }
    .notice { padding:.9rem 1rem; border-left:4px solid var(--gold); background:#fffaf0;
              border-radius:6px 12px 12px 6px; color:#5b5140; margin:1rem 0; }
    .fact { padding:1rem 1.1rem; background:#fff; border:1px solid #e1e8e3; border-radius:14px; }
    .principle { padding:1rem 1.1rem; background:var(--mist); border-radius:14px; margin:.55rem 0; }
    .status { color:var(--sage); font-weight:700; font-size:.82rem; text-transform:uppercase; }
    .question { font-size:1.13rem; line-height:1.55; padding:1rem 1.2rem;
                border-left:4px solid var(--sage); background:white; border-radius:6px 14px 14px 6px;
                margin:.7rem 0; }
    .law { padding:1rem 1.1rem; background:#fff; border:1px solid #e1e8e3;
           border-radius:14px; margin:.65rem 0; }
    div.stButton > button { background:#536f62; color:white; border-radius:999px; border:0;
                           font-weight:700; padding:.65rem 1.35rem; }
    div.stButton > button:hover { background:#40594e; color:white; border:0; }
    footer { visibility:hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


PRINCIPLES = {
    "Conciencia": "Distingue hechos, interpretación, emociones y expectativas.",
    "Coherencia": "Examina la relación entre intención, palabras, acciones y consecuencias.",
    "Responsabilidad": "Separa lo que depende de la persona, de otros y de nadie.",
    "Flexibilidad": "Explora qué aceptar, proteger, transformar o dejar marchar.",
    "Reciprocidad": "Considera los efectos sobre uno mismo, otras personas y el entorno.",
    "Trascendencia": "Reconoce la incertidumbre y el significado sin presentar creencias como hechos.",
}

LAWS = [
    "Como es arriba, así es abajo", "Como es dentro, así es fuera", "Petición",
    "Atracción", "Resistencia", "Reflejo", "Proyección", "Apego", "Atención",
    "Flujo", "Abundancia", "Claridad", "Intención", "Prosperidad", "Manifestación",
    "Éxito", "Equilibrio y polaridad", "Karma", "Reencarnación", "Responsabilidad",
    "Discernimiento", "Afirmación", "Oración", "Meditación", "Desafío",
    "Frecuencia o vibración", "Milagros", "Sanación", "Purificación", "Perspectiva",
    "Gratitud", "Bendiciones", "Decreto", "Fe", "Gracia", "Unidad",
]

SYSTEM_PROMPT = f"""
Eres Brújula 36, una guía de discernimiento inspirada críticamente en las 36 leyes
espirituales expuestas por Diana Cooper. No eres una autoridad religiosa, terapeuta,
jurista ni oráculo. No juzgas a la persona ni decides por ella.

Analiza mediante estos seis principios:
{json.dumps(PRINCIPLES, ensure_ascii=False)}

Leyes disponibles (usa solo entre 2 y 5 realmente pertinentes):
{json.dumps(LAWS, ensure_ascii=False)}

REGLAS OBLIGATORIAS
- Trata como hechos únicamente acciones, palabras o circunstancias explícitamente aportadas.
  Una percepción, generalización, intención atribuida o explicación causal pertenece a interpretaciones.
- Distingue la emoción propia del comportamiento ajeno. Evita expresiones como "me hizo sentir";
  usa formulaciones como "sentí X cuando ocurrió Y".
- No afirmes que alguien atrajo un abuso, enfermedad, pobreza, accidente o desgracia.
- No conviertas karma, vibración, milagros, reencarnación o intervención divina en hechos.
- Si aparecen violencia, autolesión, peligro, delito o urgencia médica, prioriza seguridad y ayuda profesional.
- Distingue siempre un límite protector de un castigo indirecto. Si la intención no está clara,
  preséntalo como pregunta o tensión, nunca como conclusión.
- No conviertas la reciprocidad en contabilidad afectiva. Ayudar no crea automáticamente una deuda,
  pero revisar la disponibilidad propia puede evitar sobrecarga y resentimiento.
- Evita expresiones vagas como "administrar tu energía" cuando puedas decir disponibilidad,
  límites, atención, tiempo o implicación emocional.
- No fuerces los seis principios. Usa solo estos estados: "Alineación", "Tensión",
  "Posibilidad de desarrollo" y "No determinable".
- Evita absolutos y lenguaje culpabilizador. Ofrece posibilidades, no sentencias.
- Cada ley seleccionada debe estar claramente justificada en el caso. Explica por separado
  su utilidad interpretativa y si su contenido es orientación ética/psicológica, metáfora o creencia metafísica.
- Contesta en español claro, sereno, concreto y sin grandilocuencia.

Devuelve EXCLUSIVAMENTE JSON válido con esta estructura exacta:
{{
  "comprension": "resumen neutral",
  "hechos": ["hecho explícito"],
  "interpretaciones": ["posible interpretación, expresada con cautela"],
  "informacion_faltante": ["dato relevante no conocido"],
  "principios": [
    {{"nombre":"Conciencia", "estado":"Alineación|Tensión|Posibilidad de desarrollo|No determinable", "lectura":"..."}}
  ],
  "leyes": [
    {{"nombre":"una ley de la lista", "plano_interpretativo":"...", "lectura_critica":"orientación ética/psicológica o creencia metafísica"}}
  ],
  "tension_central": "...",
  "preguntas": ["entre 2 y 4 preguntas abiertas"],
  "alternativas": ["entre 1 y 3 posibilidades concretas"],
  "cierre": "recordatorio breve de autonomía"
}}
Incluye exactamente los seis principios, en el orden dado.
En las alternativas, aclara cuando una retirada puede ser cuidado propio y cuando podría
funcionar como represalia. Formula las preguntas sin atribuir a otra persona la autoría
directa de las emociones del usuario.
""".strip()


def secret(name, default=None):
    try:
        return st.secrets.get(name, default)
    except Exception:
        return os.getenv(name, default)


def extract_json(text):
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.I | re.S)
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start < 0 or end < 0:
        raise ValueError("La respuesta no contiene un análisis estructurado.")
    return json.loads(cleaned[start : end + 1])


def analyze_with_gemini(case, context):
    api_key = secret("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta configurar GEMINI_API_KEY en los secretos de la aplicación.")
    model = secret("GEMINI_MODEL", "gemini-3.6-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    user_text = f"SITUACIÓN:\n{case}\n\nCONTEXTO ADICIONAL:\n{context or 'No aportado.'}"
    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": user_text}]}],
        "generationConfig": {"temperature": 0.25, "responseMimeType": "application/json"},
    }
    response = requests.post(url, params={"key": api_key}, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return extract_json(data["candidates"][0]["content"]["parts"][0]["text"])


def render_result(data):
    st.divider()
    st.subheader("Lectura de la situación")
    st.markdown(
        f'<div class="fact">{escape(str(data.get("comprension", "")))}</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    for col, title, key in zip(
        cols,
        ["Hechos aportados", "Interpretaciones posibles", "Información que falta"],
        ["hechos", "interpretaciones", "informacion_faltante"],
    ):
        with col:
            st.markdown(f"**{title}**")
            for item in data.get(key, []):
                st.markdown(f"- {item}")

    st.subheader("Los seis principios")
    for item in data.get("principios", []):
        st.markdown(
            f'<div class="principle"><span class="status">{escape(str(item.get("estado", "")))}</span>'
            f'<h3>{escape(str(item.get("nombre", "")))}</h3>'
            f'<div>{escape(str(item.get("lectura", "")))}</div></div>',
            unsafe_allow_html=True,
        )

    st.subheader("Leyes especialmente relacionadas")
    for law in data.get("leyes", []):
        st.markdown(
            f'<div class="law"><h3>{escape(str(law.get("nombre", "Ley relacionada")))}</h3>'
            f'<p><b>Lectura interpretativa:</b> {escape(str(law.get("plano_interpretativo", "")))}</p>'
            f'<p><b>Lectura crítica:</b> {escape(str(law.get("lectura_critica", "")))}</p></div>',
            unsafe_allow_html=True,
        )

    st.subheader("Tensión central")
    st.info(data.get("tension_central", ""))

    st.subheader("Preguntas para discernir")
    for question in data.get("preguntas", []):
        st.markdown(
            f'<div class="question">{escape(str(question))}</div>',
            unsafe_allow_html=True,
        )

    st.subheader("Posibles formas de avanzar")
    for alternative in data.get("alternativas", []):
        st.markdown(f"- {alternative}")
    st.caption(data.get("cierre", "La decisión permanece siempre en tus manos."))


st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Discernimiento consciente</div>
      <h1>Brújula 36</h1>
      <div class="subtitle">Contempla tus decisiones desde seis principios de conciencia,
      inspirados en las 36 leyes espirituales y examinados con una mirada crítica.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="notice"><b>No dicta qué es espiritualmente correcto.</b> Te ayuda a distinguir '
    'hechos, interpretaciones, responsabilidades, consecuencias y creencias.</div>',
    unsafe_allow_html=True,
)

with st.form("case_form"):
    case = st.text_area(
        "Describe una acción, decisión o conflicto",
        height=170,
        placeholder="Ejemplo: Estoy pensando en dejar de hablar con mi hermana porque nunca reconoce sus errores...",
    )
    context = st.text_area(
        "Contexto adicional (opcional)",
        height=90,
        placeholder="Qué ocurrió, quiénes participan, qué deseas proteger o conseguir...",
    )
    consent = st.checkbox("Comprendo que recibiré una orientación reflexiva, no un veredicto.")
    submitted = st.form_submit_button("Abrir la reflexión")

if submitted:
    if len(case.strip()) < 20:
        st.warning("Describe la situación con algo más de detalle para poder analizarla.")
    elif not consent:
        st.warning("Confirma que comprendes el carácter reflexivo del análisis.")
    else:
        try:
            with st.spinner("Contemplando la situación desde distintas perspectivas…"):
                result = analyze_with_gemini(case.strip(), context.strip())
            st.session_state["last_result"] = result
        except requests.HTTPError as exc:
            detail = exc.response.text[:300] if exc.response is not None else str(exc)
            st.error(f"No fue posible completar el análisis. Revisa la configuración del modelo. {detail}")
        except Exception as exc:
            st.error(str(exc))

if st.session_state.get("last_result"):
    render_result(st.session_state["last_result"])

with st.sidebar:
    st.header("Los seis principios")
    for name, description in PRINCIPLES.items():
        st.markdown(f"**{name}**  \n{description}")
    st.divider()
    st.caption("Inspirada en el marco espiritual de Diana Cooper. Las afirmaciones metafísicas se presentan como creencias, no como hechos científicos.")
