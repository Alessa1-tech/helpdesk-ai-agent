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

- Python
- OpenAI API (GPT-3.5)
- Streamlit
- python-dotenv

## ⚙️ Instalación

1. Clona el repositorio
2. Crea el entorno virtual e instala dependencias
3. Crea un archivo `.env` con tu API key de OpenAI: `OPENAI_API_KEY=tu-api-key`
4. Ejecuta `streamlit run app.py`

## 👤 Autor

Alejandro Espier — [LinkedIn](https://www.linkedin.com/in/alejandro-espier-52863b363/)