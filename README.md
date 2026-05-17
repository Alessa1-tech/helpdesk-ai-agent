# 🎧 Helpdesk AI Agent

Agente de IA que analiza tickets de soporte IT y devuelve automáticamente categoría, prioridad, pasos de resolución y decisión de escalado.

## 🎯 Problema que resuelve

En un helpdesk real, el técnico recibe descripciones de incidencias en texto libre y tiene que clasificarlas manualmente. Este agente automatiza ese proceso en segundos.

## 🚀 Demo

Escribe cualquier incidencia IT y el agente responde con:
- 📋 Categoría del problema
- 🔴 Prioridad (Crítica / Alta / Media / Baja)
- 🔧 Pasos de resolución
- ⚡ Si escalar o no a N2

## 🛠️ Stack

- Python 3.10+
- OpenAI API (GPT-3.5)
- Streamlit
- python-dotenv

## ⚙️ Instalación paso a paso

### 1. Requisitos previos

Necesitas tener instalado:
- [Python 3.10 o superior](https://www.python.org/downloads/) — durante la instalación marca obligatoriamente **"Add Python to PATH"**
- [Git](https://git-scm.com/download/win) — deja todas las opciones por defecto

Verifica que están instalados abriendo PowerShell y ejecutando:
```bash
python --version
git --version
Tiene que devolverte un número de versión en cada uno. Si da error, revisa que marcaste "Add to PATH" durante la instalación.

2. Clona el repositorio
Abre PowerShell y ejecuta:

git clone https://github.com/Alessa1-tech/helpdesk-ai-agent
cd helpdesk-ai-agent
3. Crea el entorno virtual
python -m venv venv
⚠️ Error frecuente en Windows: Si al activar el entorno virtual te aparece un error de permisos como UnauthorizedAccess o cannot be loaded because running scripts is disabled, ejecuta primero este comando en PowerShell:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Escribe S y pulsa Enter. Después continúa con el paso siguiente.

Actívalo:

Windows:
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate
Verás (venv) al inicio de la línea — eso confirma que está activo. No continúes sin verlo.

4. Instala las dependencias
pip install -r requirements.txt
Espera a que termine. Verás una lista de paquetes instalándose.

5. Configura tu API Key de OpenAI
Crea una cuenta en platform.openai.com
Ve a API Keys → Create new secret key
Copia la key — empieza por sk-...
⚠️ Importante: guarda la key en ese momento porque OpenAI solo te la muestra una vez.

Crea un archivo llamado .env en la carpeta raíz del proyecto
Escribe dentro exactamente esto:
OPENAI_API_KEY=tu-api-key-aqui
Sustituye tu-api-key-aqui por tu key real. Sin espacios, sin comillas.

⚠️ Nunca subas el archivo .env a GitHub. Ya está protegido por el .gitignore del proyecto, pero nunca lo compartas.

6. Ejecuta la aplicación
streamlit run app.py
Se abrirá automáticamente en tu navegador en http://localhost:8501

⚠️ Si no se abre automáticamente: copia y pega http://localhost:8501 directamente en tu navegador.

👤 Autor
Alejandro Espier — LinkedIn