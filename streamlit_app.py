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
            # 1. TOMAR FOTO DEL TIEMPO DEL ARCHIVO ANTES DE EJECUTAR
            ruta_img = "reporte_grafico.png"
            tiempo_antes = 0
            if os.path.exists(ruta_img):
                tiempo_antes = os.path.getmtime(ruta_img)

            # 2. INVOCAR AL AGENTE
            respuesta = agente_actual.invoke({"input": prompt})
            texto_respuesta = respuesta['output']
            
            # 3. VERIFICAR SI EL ARCHIVO CAMBIÓ
            tiempo_despues = 0
            hay_nuevo_grafico = False
            
            if os.path.exists(ruta_img):
                tiempo_despues = os.path.getmtime(ruta_img)
                # Si el tiempo es mayor, el archivo fue modificado recientemente
                if tiempo_despues > tiempo_antes:
                    hay_nuevo_grafico = True

            # 4. MOSTRAR RESPUESTA Y GRÁFICO
            message_placeholder.markdown(texto_respuesta)
            
            # Guardar texto en historial
            msg_data = {"role": "assistant", "content": texto_respuesta}
            
            if hay_nuevo_grafico:
                # Usamos un timestamp en la URL para engañar al caché del navegador
                # y forzar que muestre la imagen nueva
                st.image(ruta_img, caption="Gráfico Generado")
                
                # Guardamos la referencia en el historial
                msg_data["image"] = ruta_img
            
            st.session_state.messages.append(msg_data)
            
        except Exception as e:
            error_msg = f"❌ Ocurrió un error: {str(e)}"
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})