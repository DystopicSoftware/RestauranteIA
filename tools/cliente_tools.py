from langchain.tools import Tool
from funciones import productos_ops, ventas_ops

herramientas_cliente = [
    Tool(name="VerMenu", func=lambda x: productos_ops.ver_menu_completo(), description="Ver lista de precios."),
    Tool(name="VerDisponibilidad", func=productos_ops.ver_disponibilidad_producto, description="Chequear si hay stock de un producto."),
    Tool(name="VerIngredientes", func=productos_ops.ver_ingredientes_producto, description="Ver qué contiene un producto."),
    Tool(name="VerProductosDisponibles", func=lambda x: productos_ops.ver_productos_disponibles(), description="Lista lo que se puede comprar hoy."),
    
    Tool(name="CotizarPedido", func=ventas_ops.cotizar_pedido, description="Calcula total de un pedido libre."),
    Tool(name="RegistrarPedido", func=ventas_ops.registrar_pedido, description="Realiza la compra y descuenta inventario.")
]