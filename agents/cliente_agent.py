from langchain.agents import initialize_agent, AgentType
from config.settings import llm
from tools.cliente_tools import herramientas_cliente

# Definimos un mensaje de instrucciones (Prompt) para corregir a Llama3
INSTRUCCIONES_FORMATO = """
Tienes acceso a las siguientes herramientas:

{tools}

Para usar una herramienta, DEBES usar el siguiente formato EXACTO:

Thought: ¿Qué debo hacer? Pensamiento sobre la acción a tomar.
Action: el nombre de la herramienta para usar, debe ser uno de [{tool_names}]. NO escribas paréntesis ().
Action Input: la entrada para la herramienta.
Observation: el resultado de la herramienta.

EJEMPLO CORRECTO:
Thought: Necesito ver el inventario.
Action: VerInventario
Action Input: 

EJEMPLO INCORRECTO (NO HAGAS ESTO):
Action: VerInventario()
Action: VerInventario(x)

Cuando tengas una respuesta final para el humano, usa el formato:
Final Answer: tu respuesta aquí.

¡Comienza!
"""

agente_cliente = initialize_agent(
    tools=herramientas_cliente,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,  # <--- AGREGA ESTO
    agent_kwargs={
        "prefix": INSTRUCCIONES_FORMATO # <--- AQUÍINYECTAMOS LA INSTRUCCIÓN
    },
)