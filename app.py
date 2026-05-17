import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import re
import random
import string

load_dotenv()

# Funciona tanto en local como en Streamlit Cloud
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    N8N_WEBHOOK_URL = st.secrets["N8N_WEBHOOK_URL"]
except:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

client = OpenAI(api_key=OPENAI_API_KEY)

def validar_email(email):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def generar_numero_ticket():
    letras = ''.join(random.choices(string.ascii_uppercase, k=2))
    numeros = ''.join(random.choices(string.digits, k=4))
    return f"IT-{letras}{numeros}"

SYSTEM_PROMPT = """Eres un agente experto en soporte IT y helpdesk de empresa.
Tu objetivo es recopilar toda la informacion necesaria para resolver o escalar una incidencia.

FASE 1 - RECOPILACION DE INFORMACION:
Antes de clasificar, asegurate de tener suficiente contexto. Haz preguntas especificas una a una.
Ejemplos de informacion util:
- Desde cuando ocurre el problema
- Si ha pasado antes
- Que pasos ha intentado el usuario
- Si afecta solo a ese usuario o a mas
- El dispositivo o sistema afectado
- Si hay algun mensaje de error visible

Cuando tengas suficiente informacion para resolver o escalar, responde con este formato exacto:

[ANALISIS_COMPLETO]
TIPO: [TIPO_A / TIPO_B / TIPO_C]
Categoria: [categoria del problema]
Prioridad: [Critica / Alta / Media / Baja]
Motivo prioridad: [motivo breve]
Respuesta al usuario: [mensaje final al usuario]
Resumen para IT: [resumen estructurado del problema con todo el contexto recopilado]
Pasos intentados: [lo que el usuario ya ha probado]
Impacto: [si afecta a mas usuarios o solo a este]

FASE 2 - CLASIFICACION:
TIPO_A: El usuario puede resolverlo COMPLETAMENTE solo.
TIPO_B: Requiere intervencion del equipo IT.
TIPO_C: El usuario pide hablar con un tecnico humano.

EN CASO DE DUDA: clasifica siempre como TIPO_B.

IMPORTANTE:
- Detecta el idioma del usuario y responde siempre en ese mismo idioma
- Haz solo UNA pregunta a la vez
- Si ya tienes suficiente informacion, no hagas mas preguntas
- No uses el formato [ANALISIS_COMPLETO] hasta tener toda la informacion necesaria"""

st.set_page_config(page_title="Helpdesk AI Agent", page_icon="🎧")
st.title("🎧 Helpdesk AI Agent")
st.write("Describe tu incidencia y te ayudamos.")

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
if "ticket_cerrado" not in st.session_state:
    st.session_state.ticket_cerrado = False
if "numero_ticket" not in st.session_state:
    st.session_state.numero_ticket = None
if "datos_usuario" not in st.session_state:
    st.session_state.datos_usuario = {}
if "esperando_respuesta" not in st.session_state:
    st.session_state.esperando_respuesta = False

if not st.session_state.datos_usuario:
    with st.form("form_inicio"):
        nombre = st.text_input("Tu nombre")
        email = st.text_input("Tu email corporativo")
        problema = st.text_area("Describe tu incidencia", height=100, placeholder="Ej: No me enciende el ordenador...")
        enviado = st.form_submit_button("Iniciar")

    if enviado:
        if not nombre or not email or not problema:
            st.warning("Por favor rellena todos los campos.")
        elif not validar_email(email):
            st.error("El email no es valido. Debe tener el formato usuario@empresa.com")
        else:
            st.session_state.datos_usuario = {"nombre": nombre, "email": email}
            st.session_state.mensajes.append({"role": "user", "content": problema})
            st.session_state.esperando_respuesta = True
            st.rerun()

else:
    nombre = st.session_state.datos_usuario["nombre"]
    email = st.session_state.datos_usuario["email"]

    for msg in st.session_state.mensajes:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        elif msg["role"] == "assistant" and "[ANALISIS_COMPLETO]" not in msg["content"]:
            with st.chat_message("assistant"):
                st.write(msg["content"])

    if st.session_state.ticket_cerrado:
        if st.session_state.numero_ticket == "RESUELTA":
            st.success("Incidencia resuelta. Si necesitas mas ayuda abre una nueva incidencia.")
        else:
            st.info(f"Tu ticket **{st.session_state.numero_ticket}** ha sido enviado al equipo de IT. Te contactaran pronto en **{email}**.")
        if st.button("Nueva incidencia"):
            st.session_state.mensajes = []
            st.session_state.ticket_cerrado = False
            st.session_state.numero_ticket = None
            st.session_state.datos_usuario = {}
            st.session_state.esperando_respuesta = False
            st.rerun()

    elif st.session_state.esperando_respuesta:
        st.session_state.esperando_respuesta = False
        with st.spinner("Analizando..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.mensajes
            )
            respuesta = response.choices[0].message.content
            st.session_state.mensajes.append({"role": "assistant", "content": respuesta})

            if "[ANALISIS_COMPLETO]" in respuesta:
                lineas = respuesta.split("\n")
                tipo = ""
                prioridad = ""
                resumen_it = ""
                pasos = ""
                impacto = ""

                for linea in lineas:
                    if "TIPO_A" in linea:
                        tipo = "TIPO_A"
                    elif "TIPO_B" in linea:
                        tipo = "TIPO_B"
                    elif "TIPO_C" in linea:
                        tipo = "TIPO_C"
                    if "Prioridad:" in linea and "Motivo" not in linea:
                        prioridad = linea.split("Prioridad:")[-1].strip()
                    if "Resumen para IT:" in linea:
                        resumen_it = linea.split("Resumen para IT:")[-1].strip()
                    if "Pasos intentados:" in linea:
                        pasos = linea.split("Pasos intentados:")[-1].strip()
                    if "Impacto:" in linea:
                        impacto = linea.split("Impacto:")[-1].strip()

                if tipo == "TIPO_A":
                    st.session_state.ticket_cerrado = True
                    st.session_state.numero_ticket = "RESUELTA"

                elif tipo in ["TIPO_B", "TIPO_C"]:
                    numero_ticket = generar_numero_ticket()
                    st.session_state.numero_ticket = numero_ticket
                    st.session_state.ticket_cerrado = True

                    historial = "\n".join([
                        f"{'Usuario' if m['role'] == 'user' else 'Agente'}: {m['content']}"
                        for m in st.session_state.mensajes
                        if "[ANALISIS_COMPLETO]" not in m["content"]
                    ])

                    payload = {
                        "numero_ticket": numero_ticket,
                        "nombre": nombre,
                        "email": email,
                        "tipo": tipo,
                        "prioridad": prioridad,
                        "resumen": resumen_it,
                        "pasos_intentados": pasos,
                        "impacto": impacto,
                        "historial": historial
                    }
                    requests.post(N8N_WEBHOOK_URL, json=payload)

        st.rerun()

    else:
        respuesta_usuario = st.chat_input("Escribe tu respuesta...")
        if respuesta_usuario:
            st.session_state.mensajes.append({"role": "user", "content": respuesta_usuario})
            st.session_state.esperando_respuesta = True
            st.rerun()