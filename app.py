import sys
# Asegura que Python encuentre los módulos
sys.path.append(".") 

from database.db_manager import cargar_datos_iniciales
from agents.admin_agent import agente_admin
from agents.cliente_agent import agente_cliente

def main():
    # 1. Cargar Datos
    cargar_datos_iniciales()
    
    print("\n=== 🍔 RESTAURANTE IA (Modular) ===")
    print("1. Modo Admin")
    print("2. Modo Cliente")
    op = input("Selecciona opción (1 o 2): ").strip()
    
    if op == "1":
        agente = agente_admin
        nombre = "ADMIN"
        print("\n✅ Modo ADMIN activado (Inventario, KPIs, Gráficos)")
    elif op == "2":
        agente = agente_cliente
        nombre = "CLIENTE"
        print("\n✅ Modo CLIENTE activado (Pedidos, Menú)")
    else:
        print("❌ Opción inválida")
        return
    
    print(f"\n🤖 Chat {nombre} iniciado.")
    print("📝 Escribe 'salir' para terminar.\n")
    
    while True:
        try:
            pregunta = input(f"\n{nombre} > ").strip()
            if pregunta.lower() in ["salir", "exit"]:
                break
            if not pregunta: continue
            
            print("🤔 Pensando...")
            res = agente.invoke({"input": pregunta})
            print(f"🤖 IA: {res['output']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()