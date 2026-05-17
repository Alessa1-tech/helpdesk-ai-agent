import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

SYSTEM_PROMPT = """Eres un agente experto en soporte IT y helpdesk de empresa.

REGLAS DE CLASIFICACION - siguelas estrictamente:

TIPO_A: El usuario puede resolverlo COMPLETAMENTE solo, sin ninguna intervencion del equipo IT.
Ejemplos: limpiar cache del navegador, ajustar brillo de pantalla, conectar auriculares bluetooth.

TIPO_B: Requiere intervencion del equipo IT. Clasifica aqui SIEMPRE que:
- Implique contrasenas de dominio, Windows, M365, VPN o cualquier sistema corporativo
- Necesite hardware fisico (auriculares, teclado, raton, monitor, portatil)
- Requiera instalacion de software
- Implique permisos, accesos o cuentas corporativas
- El usuario no pueda continuar trabajando

TIPO_C: El usuario pide explicitamente hablar con un tecnico humano.

EN CASO DE DUDA: clasifica siempre como TIPO_B.

Responde SIEMPRE en este formato exacto:

TIPO: [TIPO_A / TIPO_B / TIPO_C]
Categoria: [categoria del problema]
Prioridad: [Critica / Alta / Media / Baja] - [motivo]
Respuesta al usuario: [mensaje directo al usuario explicando que pasara]
Notas para IT: [solo si es TIPO_B o TIPO_C - informacion relevante para el tecnico]"""

st.set_page_config(page_title="Helpdesk AI Agent", page_icon="🎧")
st.title("🎧 Helpdesk AI Agent")
st.write("Describe tu incidencia y te ayudamos.")

nombre = st.text_input("Tu nombre")
email = st.text_input("Tu email")
ticket = st.text_area("Descripcion de la incidencia", height=150, placeholder="Ej: Necesito unos auriculares nuevos...")

if st.button("Enviar"):
    if not nombre or not email or not ticket:
        st.warning("Por favor rellena todos los campos.")
    else:
        with st.spinner("Analizando tu incidencia..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": ticket}
                ]
            )

            resultado = response.choices[0].message.content
            lineas = resultado.split("\n")

            tipo = ""
            for linea in lineas:
                if "TIPO_A" in linea:
                    tipo = "TIPO_A"
                elif "TIPO_B" in linea:
                    tipo = "TIPO_B"
                elif "TIPO_C" in linea:
                    tipo = "TIPO_C"

            respuesta_usuario = ""
            for linea in lineas:
                if "Respuesta al usuario:" in linea:
                    respuesta_usuario = linea.split("Respuesta al usuario:")[-1].strip()

            if tipo in ["TIPO_B", "TIPO_C"]:
                payload = {
                    "nombre": nombre,
                    "email": email,
                    "incidencia": ticket,
                    "tipo": tipo,
                    "analisis": resultado
                }
                requests.post(N8N_WEBHOOK_URL, json=payload)

            st.success("Incidencia recibida")
            if respuesta_usuario:
                st.info(respuesta_usuario)
            else:
                st.markdown(resultado)