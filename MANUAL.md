# Manual: Helpdesk AI Agent con n8n

Guia completa para construir un agente de helpdesk con IA que clasifica tickets y envia notificaciones automaticas por email via n8n.

---

## Que construimos

Un agente de soporte IT que:
- Recibe la descripcion de una incidencia en texto libre
- La clasifica automaticamente en TIPO_A, TIPO_B o TIPO_C
- Responde al usuario con un mensaje claro
- Si la incidencia necesita IT, envia un email automatico con todos los detalles via n8n

---

## Stack utilizado

- Python 3.10+
- OpenAI API (GPT-3.5)
- Streamlit (interfaz visual)
- python-dotenv (gestion de variables de entorno)
- n8n cloud (automatizacion)
- Gmail (notificaciones)

---

## PASO 1 - Crear el repositorio en GitHub

1. Ve a github.com y haz click en "New"
2. Rellena:
   - Repository name: helpdesk-ai-agent
   - Description: AI agent that classifies and resolves IT support tickets
   - Public
   - Marca "Add a README file"
   - En "Add .gitignore" selecciona Python
3. Click en "Create repository"

---

## PASO 2 - Clonar el repositorio en tu maquina

Abre PowerShell y ejecuta:

```bash
cd Desktop
git clone git@github.com:TU-USERNAME/helpdesk-ai-agent.git
cd helpdesk-ai-agent
code .
```

Esto abre VS Code con la carpeta del proyecto.

---

## PASO 3 - Crear el entorno virtual

En la terminal de VS Code:

```bash
python -m venv venv
```

> Error frecuente en Windows: si aparece "UnauthorizedAccess" al activar, ejecuta primero:
> ```bash
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> Escribe S y pulsa Enter.

Activa el entorno:

```bash
venv\Scripts\activate
```

Veras (venv) al inicio de la linea. No continues sin verlo.

---

## PASO 4 - Instalar dependencias

```bash
pip install openai streamlit python-dotenv requests
```

---

## PASO 5 - Crear los archivos del proyecto

```bash
New-Item .env -ItemType File
New-Item .env.example -ItemType File
New-Item app.py -ItemType File
New-Item requirements.txt -ItemType File
```

---

## PASO 6 - Configurar requirements.txt

Abre requirements.txt y escribe:

```
openai
streamlit
python-dotenv
requests
```

---

## PASO 7 - Crear el workflow en n8n

1. Abre tu cuenta de n8n cloud
2. Click en "New workflow"
3. Añade un nodo "Webhook"
4. Configura:
   - HTTP Method: POST
5. Copia la Test URL para usarla en el paso siguiente
6. Guarda la Production URL para cuando el workflow este publicado

---

## PASO 8 - Configurar el archivo .env

Crea tu API key en platform.openai.com y abre el archivo .env:

```
OPENAI_API_KEY=sk-tu-api-key-aqui
N8N_WEBHOOK_URL=https://tu-instancia-n8n/webhook/tu-id
```

> Importante: usa la Production URL de n8n, no la Test URL, para que funcione sin modo test activo.

Abre .env.example y escribe:

```
OPENAI_API_KEY=tu-api-key-aqui
N8N_WEBHOOK_URL=tu-webhook-url-aqui
```

---

## PASO 9 - Codigo principal (app.py)

Abre app.py y pega este codigo:

```python
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
```

---

## PASO 10 - Configurar el nodo Gmail en n8n

1. En n8n, añade un nodo "Gmail" conectado al Webhook
2. Selecciona la accion "Send a message"
3. Conecta tu cuenta de Gmail via OAuth2
4. Configura:
   - To: tu-email@gmail.com
   - Subject: Nuevo ticket IT - {{ $json.body.tipo }} - {{ $json.body.nombre }}
   - Email Type: HTML
   - Message:
```html
<h2>Nuevo ticket de soporte IT</h2>
<p><b>Nombre:</b> {{ $json.body.nombre }}</p>
<p><b>Email:</b> {{ $json.body.email }}</p>
<p><b>Tipo:</b> {{ $json.body.tipo }}</p>
<p><b>Incidencia:</b> {{ $json.body.incidencia }}</p>
<hr>
<h3>Analisis de la IA:</h3>
<p>{{ $json.body.analisis }}</p>
```
5. Guarda el workflow y publícalo (toggle "Published")

---

## PASO 11 - Ejecutar la aplicacion

```bash
streamlit run app.py
```

Se abre automaticamente en http://localhost:8501

> Si no se abre: copia y pega http://localhost:8501 en el navegador.

---

## PASO 12 - Subir a GitHub

```bash
pip freeze > requirements.txt
git add .
git commit -m "Add helpdesk AI agent with n8n webhook integration"
git push
```

---

## Como funciona el sistema completo

```
Usuario rellena el formulario
        |
        v
OpenAI clasifica la incidencia
        |
        v
TIPO_A --> Responde al usuario con instrucciones
TIPO_B --> Llama al webhook de n8n + responde al usuario
TIPO_C --> Llama al webhook de n8n + responde al usuario
        |
        v
n8n recibe los datos y envia email a IT
        |
        v
IT recibe email con nombre, email, incidencia y analisis completo
```

---

## Errores frecuentes y soluciones

**UnauthorizedAccess al activar venv:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**ModuleNotFoundError openai:**
```bash
pip install openai
```

**n8n no recibe datos en modo test:**
Asegurate de hacer click en "Listen for test event" ANTES de enviar desde la app. El modo test solo escucha durante 2 minutos.

**n8n no recibe datos en produccion:**
Verifica que estas usando la Production URL en el .env, no la Test URL.

**Token de Gmail expirado:**
Ve al nodo Gmail en n8n, click en el lapiz de Credential y crea una nueva credencial con "Create new credential".

---

## Autor

Alejandro Espier - https://www.linkedin.com/in/alejandro-espier-52863b363/
