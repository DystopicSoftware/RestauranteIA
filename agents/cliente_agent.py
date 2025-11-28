from langchain.agents import initialize_agent, AgentType
from config.settings import llm
from tools.cliente_tools import herramientas_cliente

agente_cliente = initialize_agent(
    tools=herramientas_cliente,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)