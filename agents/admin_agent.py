from langchain.agents import initialize_agent, AgentType
from config.settings import llm
from tools.admin_tools import herramientas_admin

agente_admin = initialize_agent(
    tools=herramientas_admin,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)