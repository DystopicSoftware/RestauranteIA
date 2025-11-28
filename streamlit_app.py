import streamlit as st
import os
import sys

# Aseguramos que Python encuentre los módulos
sys.path.append(".") 

from database.db_manager import cargar_datos_iniciales
from agents.admin_agent import agente_admin
from agents.cliente_agent import agente_cliente

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="RestauranteIA",
    page_icon="🍔",
    layout="wide"
)

# --- INICIALIZACIÓN ---
if "datos_cargados" not in st.session_state:
    cargar_datos_iniciales()
    st.session_state.datos_cargados = True

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3075/3075977.png", width=100)
    st.title("RestauranteIA 🤖")
    st.markdown("---")
    
    # Selector de Modo
    modo = st.radio("Selecciona tu rol:", ["👨‍💼 Administrador", "🍽️ Cliente"])
    
    # Botón para limpiar chat
    if st.button("🧹 Limpiar Chat", type="primary"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.caption(f"🐍 Python {sys.version.split()[0]}")
    st.caption("Powered by Ollama Llama3")

# --- LÓGICA DEL CHAT ---

# 1. Definir Agente según el modo
if "Administrador" in modo:
    agente_actual = agente_admin
    rol_actual = "admin"
    st.header("👨‍💼 Panel de Control Administrativo")
else:
    agente_actual = agente_cliente
    rol_actual = "cliente"
    st.header("🍽️ Menú y Pedidos")

# 2. Inicializar historial de mensajes si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Detectar cambio de rol para limpiar historial (opcional, para no mezclar contextos)
if "last_role" not in st.session_state:
    st.session_state.last_role = rol_actual

if st.session_state.last_role != rol_actual:
    st.session_state.messages = []
    st.session_state.last_role = rol_actual

# 4. Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Si el mensaje histórico tenía una imagen asociada
        if "image" in message:
            st.image(message["image"])

# 5. INPUT DEL USUARIO
if prompt := st.chat_input("Escribe aquí tu consulta..."):
    
    # A) Mostrar mensaje del usuario
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # B) Procesar con IA
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤔 Procesando...")
        
        try:
            # Invocar al agente LangChain
            respuesta = agente_actual.invoke({"input": prompt})
            texto_respuesta = respuesta['output']
            
            # Actualizar el placeholder con la respuesta final
            message_placeholder.markdown(texto_respuesta)
            
            # Guardar en historial
            msg_data = {"role": "assistant", "content": texto_respuesta}
            
            # C) Detectar si se generó un gráfico
            # El agente guarda la imagen en 'reporte_grafico.png'.
            # Verificamos si la respuesta del agente menciona el archivo.
            if "reporte_grafico.png" in texto_respuesta and os.path.exists("reporte_grafico.png"):
                # Mostrar imagen
                st.image("reporte_grafico.png", caption="Gráfico Generado")
                # Agregar imagen al historial para que persista
                msg_data["image"] = "reporte_grafico.png"
                
                # Opcional: Renombrar o mover la imagen para no sobrescribir historial
                # (Por simplicidad lo dejamos así, pero en prod se debería guardar con timestamp)
            
            st.session_state.messages.append(msg_data)
            
        except Exception as e:
            error_msg = f"❌ Ocurrió un error: {str(e)}"
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})