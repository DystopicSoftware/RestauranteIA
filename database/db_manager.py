import sqlite3
import pandas as pd
import os
from config.settings import DB_NAME
# Importamos los módulos de datos para poder modificarlos
import data.inventario as d_inv
import data.ventas as d_ventas
import data.productos as d_prod

def guardar_cambios():
    """
    Vuelca los DataFrames actuales al archivo SQLite.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        # Guardamos inventario
        d_inv.inventario.to_sql("inventario", conn, if_exists="replace", index=False)
        # Guardamos ventas
        d_ventas.ventas.to_sql("ventas", conn, if_exists="replace", index=False)

        # Guardamos precios simples (para persistencia básica)
        df_precios = pd.DataFrame(list(d_prod.precio_venta.items()), columns=["Producto", "Precio"])
        df_precios.to_sql("precios", conn, if_exists="replace", index=False)

        conn.close()
    except Exception as e:
        print(f"⚠️ Error guardando base de datos: {e}")

def cargar_datos_iniciales():
    """
    Carga los datos de SQLite a la memoria al iniciar.
    """
    if os.path.exists(DB_NAME):
        try:
            conn = sqlite3.connect(DB_NAME)

            # 1. Cargar Inventario
            d_inv.inventario = pd.read_sql("SELECT * FROM inventario", conn)

            # 2. Cargar Ventas
            d_ventas.ventas = pd.read_sql("SELECT * FROM ventas", conn)
            if not d_ventas.ventas.empty:
                d_ventas.ventas["Fecha"] = pd.to_datetime(d_ventas.ventas["Fecha"], format='mixed')

            # 3. Cargar Precios (Actualizamos el diccionario en memoria)
            try:
                df_precios = pd.read_sql("SELECT * FROM precios", conn)
                d_prod.precio_venta.update(dict(zip(df_precios["Producto"], df_precios["Precio"])))
            except:
                pass

            conn.close()
            print("📂 Base de datos cargada correctamente.")
        except Exception as e:
            print(f"⚠️ Error cargando BD (usando datos por defecto): {e}")
            # Si falla, se queda con lo que haya en data/*.py
    else:
        print("🆕 No se encontró base de datos. Se creará al guardar cambios.")
        guardar_cambios()