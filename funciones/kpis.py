import pandas as pd
from data.ventas import ventas
from data.productos import recetas

def ver_productos_mas_vendidos():
    if ventas.empty: return "Sin ventas."
    return ventas.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False).to_string()

def ver_ganancia_por_producto():
    if ventas.empty: return "Sin ventas."
    return ventas.groupby("Producto")["Ganancia"].sum().sort_values(ascending=False).to_string()

def ver_producto_mas_rentable():
    if ventas.empty: return "No hay ventas registradas."
    resumen = ventas.groupby("Producto")["Ganancia"].sum().sort_values(ascending=False)
    producto_top = resumen.index[0]
    ganancia_top = resumen.iloc[0]
    return f"El producto más rentable es '{producto_top}' con una ganancia total de ${ganancia_top:,.0f}."

def ver_productos_no_vendidos():
    vendidos = set(ventas["Producto"].unique())
    todos = set(recetas.keys())
    no_vendidos = sorted(todos - vendidos)
    return ", ".join(no_vendidos) if no_vendidos else "Todos los productos se han vendido."

def ver_dia_mas_ventas():
    if ventas.empty: return "Aún no hay ventas."
    por_dia = ventas.assign(Dia=ventas["Fecha"].dt.date).groupby("Dia")["Ganancia"].sum()
    if por_dia.empty: return "Aún no hay ventas."
    return f"El día con más ganancias fue {por_dia.idxmax()} (${por_dia.max():,.0f})."

def ver_ingresos_por_dia():
    if ventas.empty: return "Aún no hay ventas."
    por_dia = ventas.assign(Dia=ventas["Fecha"].dt.date).groupby("Dia")["Total"].sum()
    salida = "Ingresos por día:\n"
    for fecha, valor in por_dia.sort_index().items():
        salida += f"- {fecha}: ${valor:,.0f}\n"
    return salida

def ver_ganancias_por_producto_por_dia():
    if ventas.empty: return "Aún no hay ventas."
    return ventas.assign(Dia=ventas["Fecha"].dt.date).groupby(["Dia", "Producto"])["Ganancia"].sum().unstack(fill_value=0).to_string()

def ver_top_3_productos():
    if ventas.empty: return "Sin ventas."
    return ventas.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False).head(3).to_string()

def ver_productos_y_ventas():
    if ventas.empty: return "Sin ventas."
    return ventas.groupby("Producto").agg(Unidades=("Cantidad","sum"), Ingresos=("Total","sum"), Ganancia=("Ganancia","sum")).sort_values(by="Unidades", ascending=False).to_string()

def ver_productos_con_poca_venta(threshold=3):
    if ventas.empty: return "Sin ventas."
    resumen = ventas.groupby("Producto")["Cantidad"].sum()
    poca = resumen[resumen <= threshold]
    if poca.empty: return "No hay productos con pocas ventas."
    return str(poca)

def ver_promedio_venta_por_producto():
    if ventas.empty: return "Sin ventas."
    return ventas.groupby("Producto")["Ganancia"].mean().to_string()

def ver_ganancias_por_dia():
    if ventas.empty: return "Sin ventas."
    por_dia = ventas.assign(Dia=ventas["Fecha"].dt.date).groupby("Dia")["Ganancia"].sum()
    salida = "Ganancias por día:\n"
    for d, g in por_dia.sort_index().items():
        salida += f"- {d}: ${g:,.0f}\n"
    return salida