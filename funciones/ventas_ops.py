import pandas as pd
import data.ventas as d_ventas
import data.inventario as d_inv
import data.productos as d_prod
from database.db_manager import guardar_cambios
from utils.matching import match_producto
from utils.parsers import parsear_pedido_libre

def registrar_venta(producto: str, cantidad: int):
    oficial = match_producto(producto)
    if not oficial: return "Producto no existe."
    
    receta = d_prod.recetas.get(oficial)
    if not receta: return "Receta no encontrada."

    # Check Stock
    for ing, req in receta.items():
        st_row = d_inv.inventario[d_inv.inventario["Ingrediente"]==ing]["Stock"].values
        st = st_row[0] if len(st_row)>0 else 0
        if st < req * cantidad:
            return f"Falta stock de {ing}."
    
    # Descontar
    for ing, req in receta.items():
        d_inv.inventario.loc[d_inv.inventario["Ingrediente"]==ing, "Stock"] -= req * cantidad
    
    p = d_prod.precio_venta.get(oficial, 0)
    c = d_prod.costo_unitario.get(oficial, 0)
    tot = p * cantidad
    gan = (p - c) * cantidad
    
    nueva = {"Fecha": pd.Timestamp.now(), "Producto": oficial, "Cantidad": cantidad, "Total": tot, "Ganancia": gan}
    d_ventas.ventas = pd.concat([d_ventas.ventas, pd.DataFrame([nueva])], ignore_index=True)
    guardar_cambios()
    return f"Venta registrada: {cantidad} {oficial}. Total ${tot}."

def cotizar_pedido(entrada: str):
    items = parsear_pedido_libre(entrada)
    if not items: return "No entendí el pedido."
    
    res = ["🧾 Cotización:"]
    total = 0
    for prod, qty in items.items():
        if prod in d_prod.precio_venta:
            sub = d_prod.precio_venta[prod] * qty
            total += sub
            res.append(f"- {qty} x {prod}: ${sub:,.0f}")
        else:
            res.append(f"- {prod}: Precio no definido.")
    res.append(f"Total: ${total:,.0f}")
    return "\n".join(res)

def registrar_pedido(entrada: str):
    items = parsear_pedido_libre(entrada)
    if not items: return "No entendí el pedido."
    
    # Check global stock
    for prod, qty in items.items():
        receta = d_prod.recetas.get(prod, {})
        for ing, req in receta.items():
            st_row = d_inv.inventario[d_inv.inventario["Ingrediente"]==ing]["Stock"].values
            st = st_row[0] if len(st_row)>0 else 0
            if st < req * qty:
                return f"❌ No alcanza stock para {prod} (falta {ing})."
    
    log = []
    for prod, qty in items.items():
        res = registrar_venta(prod, qty)
        log.append(res)
    
    return "\n".join(log)

def calcular_ingredientes_para(entrada: str):
    parts = entrada.split()
    qty = 1
    if parts[-1].isdigit():
        qty = int(parts.pop())
    nom = " ".join(parts)
    prod = match_producto(nom)
    
    if not prod: return "Producto no encontrado."
    receta = d_prod.recetas.get(prod)
    if not receta: return "Receta no encontrada."
    
    res = [f"Para {qty} {prod}:"]
    for ing, val in receta.items():
        res.append(f"- {ing}: {val*qty}")
    return "\n".join(res)