import pandas as pd
from data.productos import precio_venta, costo_unitario


# ==========================================
# VENTAS INICIALES (Historial)
# ==========================================
_crudas = [
    ("2025-11-09 12:10", "Hamburguesa sencilla", 3),
    ("2025-11-09 12:25", "Papas fritas", 4),
    ("2025-11-09 13:05", "Combo hamburguesa", 2),
    ("2025-11-09 18:40", "Perro caliente", 5),
    ("2025-11-09 19:15", "Nuggets 6", 3),
    ("2025-11-10 12:00", "Hamburguesa doble", 2),
    ("2025-11-10 12:15", "Ensalada César", 3),
    ("2025-11-10 13:30", "Wrap de pollo", 2),
    ("2025-11-10 18:20", "Burrito de frijol", 4),
    ("2025-11-10 19:10", "Veggie burger", 2),
    ("2025-11-11 12:05", "Combo hamburguesa", 3),
    ("2025-11-11 12:30", "Papas fritas", 6),
    ("2025-11-11 18:45", "Hamburguesa sencilla", 4),
    ("2025-11-11 19:20", "Perro caliente", 3),
    ("2025-11-11 20:10", "Nuggets 6", 4),
    ("2025-11-12 11:55", "Ensalada César", 2),
    ("2025-11-12 12:10", "Wrap de pollo", 3),
    ("2025-11-12 13:50", "Burrito de frijol", 5),
    ("2025-11-12 19:05", "Hamburguesa doble", 3),
    ("2025-11-12 20:00", "Veggie burger", 4),
]

# Construcción del DataFrame

ventas = pd.DataFrame(_crudas, columns=["Fecha", "Producto", "Cantidad"])
ventas["Fecha"] = pd.to_datetime(ventas["Fecha"])

# Mapear datos directamente aquí para la primera ejecución
ventas["Precio_Unit"] = ventas["Producto"].map(precio_venta)
ventas["Costo_Unit"] = ventas["Producto"].map(costo_unitario)
ventas["Total"] = ventas["Cantidad"] * ventas["Precio_Unit"]
ventas["Ganancia"] = (ventas["Precio_Unit"] - ventas["Costo_Unit"]) * ventas["Cantidad"]

# Nota: Las columnas Precio_Unit, Costo_Unit, Total y Ganancia 
# se calcularán en database/db_manager.py al cargar las ventas.