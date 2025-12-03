from langchain.tools import Tool
from funciones import kpis, inventario_ops, graficos, productos_ops, ventas_ops
from funciones.graficos import generar_grafico_avanzado

# Wrappers para parseo simple
def _add_ing_wrapper(x):
    try:
        n, s, u = x.split(",")
        return inventario_ops.agregar_ingrediente(n.strip(), int(s), u.strip())
    except: return "Error formato: Nombre,Stock,Unidad"

def _update_stock_wrapper(x):
    try:
        n, s = x.split(",")
        return inventario_ops.actualizar_stock(n.strip(), int(s))
    except: return "Error formato: Nombre,NuevoStock"

herramientas_admin = [
    Tool(name="VerInventario", func=lambda x: inventario_ops.ver_inventario(), description="Muestra inventario completo."),
    Tool(name="AgregarIngrediente", func=_add_ing_wrapper, description="Formato: Nombre,Stock,Unidad"),
    Tool(name="ActualizarStock", func=_update_stock_wrapper, description="Formato: Nombre,NuevoStock"),
    Tool(name="EliminarIngrediente", func=inventario_ops.eliminar_ingrediente, description="Nombre del ingrediente a borrar."),
    
    Tool(name="ProductosMasVendidos", func=lambda x: kpis.ver_productos_mas_vendidos(), description="Ranking ventas."),
    Tool(name="GananciasPorDia", func=lambda x: kpis.ver_ganancias_por_dia(), description="Reporte ganancias diarias."),
    Tool(name="IngresosPorDia", func=lambda x: kpis.ver_ingresos_por_dia(), description="Reporte ingresos brutos diarios."),
    Tool(name="ProductoMasRentable", func=lambda x: kpis.ver_producto_mas_rentable(), description="Producto que da más ganancia."),
    
    Tool(
        name="GenerarGrafico",
        func=generar_grafico_avanzado,
        description="Genera una imagen. La entrada DEBE ser texto plano separado por coma, ej: 'barras,ventas' o 'pastel,productos'. NO uses código."
    ),
    
    Tool(name="AgregarProducto", func=productos_ops.agregar_producto_desde_texto, description="Nombre|Precio|Costo|Ing1:Q,Ing2:Q"),
    Tool(name="ActualizarPrecio", func=productos_ops.actualizar_precio_producto, description="Nombre|NuevoPrecio"),
    Tool(name="EliminarProducto", func=productos_ops.eliminar_producto, description="Nombre del producto."),
    
    Tool(name="IngredientesPara", func=ventas_ops.calcular_ingredientes_para, description="Ej: 'Hamburguesa 10'. Calcula insumos.")
]