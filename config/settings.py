import os
from langchain_ollama import ChatOllama

# ==========================================
# CONFIGURACIÓN DEL MODELO
# ==========================================
llm = ChatOllama(
    model="llama3", 
    temperature=0.0
)

# ==========================================
# CONFIGURACIÓN DE BASE DE DATOS
# ==========================================
DB_NAME = "restaurante.db"

# ==========================================
# VARIABLES DE ENTORNO (Opcional)
# ==========================================
os.environ["OPENAI_API_KEY"] = ''
os.environ["GOOGLE_API_KEY"] = ''