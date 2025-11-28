import re
import pandas as pd
import data.productos as d_prod
import data.inventario as d_inv
from database.db_manager import guardar_cambios
from utils.matching import match_producto
from utils.parsers import parse_receta_items

def ver_disponibilidad_producto(nombre_producto: str):
    prod = match_producto(nombre_producto)
    if not prod: return "Producto no encontrado."
    receta = d_prod.recetas[prod]
    faltantes = []
    for ing, cant in receta.items():
        st = d_inv.inventario[d_inv.inventario["Ingrediente"] == ing]["Stock"].values
        actual = st[0] if len(st) > 0 else 0
        if actual < cant:
            faltantes.append(ing)
    return f"✅ Disponible {prod}" if not faltantes else f"❌ Faltan para {prod}: {', '.join(faltantes)}"

def ver_precio_producto(nombre: str):
    prod = match_producto(nombre)
    if prod and prod in d_prod.precio_venta:
        return f"${d_prod.precio_venta[prod]:,.0f}"
    return "No encontrado."

def ver_ingredientes_producto(nombre: str):
    prod = match_producto(nombre)
    if not prod: return "No encontrado."
    return str(d_prod.recetas[prod])

def ver_menu_completo():
    return "\n".join([f"- {p}: ${v:,.0f}" for p, v in d_prod.precio_venta.items()])

def ver_productos_sin_carne():
    proteinas = {"Carne hamburguesa", "Pollo pechuga", "Salchicha", "Nugget"}
    sin_carne = [p for p, r in d_prod.recetas.items() if all(i not in proteinas for i in r)]
    return ", ".join(sin_carne)

def ver_productos_disponibles():
    disponibles = []
    for p, r in d_prod.recetas.items():
        ok = True
        for ing, req in r.items():
            st = d_inv.inventario[d_inv.inventario["Ingrediente"] == ing]["Stock"].values
            val = st[0] if len(st)>0 else 0
            if val < req:
                ok = False; break
        if ok: disponibles.append(p)
    return ", ".join(disponibles) if disponibles else "Nada disponible."

# --- CRUD ---
def agregar_producto_desde_texto(payload: str):
    try:
        parts = payload.split("|")
        if len(parts) != 4: return "Formato: Nombre|Precio|Costo|Ing1:1,Ing2:2"
        nom, pre, cos, rec_str = parts
        nom = nom.strip()
        receta = parse_receta_items(rec_str)
        
        # Agregar ingredientes nuevos con stock 0
        for ing in receta:
            if ing not in d_inv.inventario["Ingrediente"].values:
                nuevo = pd.DataFrame([{"Ingrediente": ing, "Stock": 0, "Unidad": "unid"}])
                d_inv.inventario = pd.concat([d_inv.inventario, nuevo], ignore_index=True)
        
        d_prod.recetas[nom] = receta
        d_prod.precio_venta[nom] = int(pre)
        d_prod.costo_unitario[nom] = int(cos)
        guardar_cambios()
        return f"Producto {nom} agregado."
    except Exception as e:
        return f"Error: {e}"

def actualizar_precio_producto(payload: str):
    try:
        nom, val = payload.split("|")
        prod = match_producto(nom)
        if prod:
            d_prod.precio_venta[prod] = int(val)
            guardar_cambios()
            return f"Precio {prod} actualizado."
        return "No existe."
    except: return "Error formato."

def actualizar_costo_producto(payload: str):
    try:
        nom, val = payload.split("|")
        prod = match_producto(nom)
        if prod:
            d_prod.costo_unitario[prod] = int(val)
            return f"Costo {prod} actualizado."
        return "No existe."
    except: return "Error formato."

def eliminar_producto(nom: str):
    prod = match_producto(nom)
    if prod:
        d_prod.recetas.pop(prod, None)
        d_prod.precio_venta.pop(prod, None)
        d_prod.costo_unitario.pop(prod, None)
        guardar_cambios()
        return f"{prod} eliminado."
    return "No encontrado."