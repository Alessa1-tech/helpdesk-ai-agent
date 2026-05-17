import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Helpdesk AI Agent", page_icon="🎧")
st.title("🎧 Helpdesk AI Agent")
st.write("Describe la incidencia y el agente la analizará automáticamente.")

ticket = st.text_area("Descripción del ticket", height=150, placeholder="Ej: No puedo acceder a mi correo desde esta mañana...")

if st.button("Analizar ticket"):
    if ticket.strip() == "":
        st.warning("Por favor escribe una incidencia.")
    else:
        with st.spinner("Analizando..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """Eres un agente experto en soporte IT y helpdesk.
Cuando recibas la descripción de una incidencia, responde SIEMPRE en este formato exacto:

📋 Categoría: [categoría del problema]
🔴 Prioridad: [Crítica / Alta / Media / Baja] — [motivo]
🔧 Pasos de resolución:
1. [paso 1]
2. [paso 2]
3. [paso 3]
⚡ Escalado: [Sí / No] — [motivo]"""
                    },
                    {
                        "role": "user",
                        "content": ticket
                    }
                ]
            )
            resultado = response.choices[0].message.content
            st.success("Análisis completado")
            st.markdown(resultado)