import pandas as pd
import data.inventario as d_inv
from database.db_manager import guardar_cambios

def agregar_ingrediente(nombre: str, stock: int, unidad: str):
    if nombre in d_inv.inventario["Ingrediente"].values:
        return f"Ya existe '{nombre}'."
    nuevo = pd.DataFrame([{"Ingrediente": nombre, "Stock": int(stock), "Unidad": unidad}])
    d_inv.inventario = pd.concat([d_inv.inventario, nuevo], ignore_index=True)
    guardar_cambios()
    return f"Ingrediente '{nombre}' agregado."

def eliminar_ingrediente(nombre: str):
    if nombre not in d_inv.inventario["Ingrediente"].values:
        return "No existe."
    d_inv.inventario = d_inv.inventario[d_inv.inventario["Ingrediente"] != nombre].reset_index(drop=True)
    guardar_cambios()
    return f"Eliminado '{nombre}'."

def actualizar_stock(nombre: str, nuevo_stock: int):
    if nombre not in d_inv.inventario["Ingrediente"].values:
        return "No existe."
    d_inv.inventario.loc[d_inv.inventario["Ingrediente"] == nombre, "Stock"] = int(nuevo_stock)
    guardar_cambios()
    return f"Stock de '{nombre}' actualizado."

def ver_inventario():
    if d_inv.inventario.empty: return "Inventario vacío."
    guardar_cambios() # Asegura snapshot
    return d_inv.inventario.to_string(index=False)