import sqlite3
import pandas as pd
import os
from config.settings import DB_NAME
# Importamos los módulos de datos para poder leerlos y modificarlos
import data.inventario as d_inv
import data.ventas as d_ventas
import data.productos as d_prod

# ---------------------------------------------------------
# 1. FUNCIÓN PARA GUARDAR (La que te faltaba)
# ---------------------------------------------------------
def guardar_cambios():
    """
    Vuelca los DataFrames actuales (en memoria) al archivo SQLite.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        
        # Guardamos inventario
        if not d_inv.inventario.empty:
            d_inv.inventario.to_sql("inventario", conn, if_exists="replace", index=False)
        
        # Guardamos ventas
        if not d_ventas.ventas.empty:
            d_ventas.ventas.to_sql("ventas", conn, if_exists="replace", index=False)

        # Guardamos precios simples (para persistencia básica)
        df_precios = pd.DataFrame(list(d_prod.precio_venta.items()), columns=["Producto", "Precio"])
        df_precios.to_sql("precios", conn, if_exists="replace", index=False)

        conn.close()
        # print("💾 Cambios guardados en base de datos.") 
    except Exception as e:
        print(f"⚠️ Error guardando base de datos: {e}")

# ---------------------------------------------------------
# 2. FUNCIÓN PARA CALCULAR COLUMNAS (La que arregla los errores de 'Ganancia')
# ---------------------------------------------------------
def enriquecer_ventas(df_ventas):
    """
    Agrega columnas calculadas (Precios, Costos, Ganancias) al DataFrame de ventas.
    """
    if df_ventas.empty:
        # Si está vacío, crear las columnas vacías para evitar error de 'Column not found'
        columns = ["Fecha", "Producto", "Cantidad", "Precio_Unit", "Costo_Unit", "Total", "Ganancia"]
        return pd.DataFrame(columns=columns)

    # 1. Mapear precios y costos desde los diccionarios de productos
    df_ventas["Precio_Unit"] = df_ventas["Producto"].map(d_prod.precio_venta)
    df_ventas["Costo_Unit"] = df_ventas["Producto"].map(d_prod.costo_unitario)

    # 2. Rellenar con 0 si algún producto no tiene precio definido
    df_ventas["Precio_Unit"] = df_ventas["Precio_Unit"].fillna(0)
    df_ventas["Costo_Unit"] = df_ventas["Costo_Unit"].fillna(0)

    # 3. Calcular Total (Ingresos) y Ganancia
    df_ventas["Total"] = df_ventas["Cantidad"] * df_ventas["Precio_Unit"]
    df_ventas["Ganancia"] = (df_ventas["Precio_Unit"] - df_ventas["Costo_Unit"]) * df_ventas["Cantidad"]

    return df_ventas

# ---------------------------------------------------------
# 3. FUNCIÓN PARA CARGAR AL INICIO
# ---------------------------------------------------------
def cargar_datos_iniciales():
    """
    Carga los datos de SQLite a la memoria al iniciar la app.
    """
    if os.path.exists(DB_NAME):
        try:
            conn = sqlite3.connect(DB_NAME)

            # A. Cargar Inventario
            try:
                d_inv.inventario = pd.read_sql("SELECT * FROM inventario", conn)
            except:
                pass # Si falla, se queda con el inventario por defecto en memoria

            # B. Cargar Ventas
            try:
                df_temporal = pd.read_sql("SELECT * FROM ventas", conn)
                if not df_temporal.empty:
                    df_temporal["Fecha"] = pd.to_datetime(df_temporal["Fecha"], format='mixed')
                
                # IMPORTANTE: Recalcular columnas matemáticas
                d_ventas.ventas = enriquecer_ventas(df_temporal)
            except:
                pass

            # C. Cargar Precios (Actualizamos el diccionario en memoria)
            try:
                df_precios = pd.read_sql("SELECT * FROM precios", conn)
                if not df_precios.empty:
                    d_prod.precio_venta.update(dict(zip(df_precios["Producto"], df_precios["Precio"])))
            except:
                pass

            conn.close()
            print("📂 Base de datos cargada y procesada correctamente.")
        except Exception as e:
            print(f"⚠️ Error cargando BD (usando datos por defecto): {e}")
    else:
        print("🆕 No se encontró base de datos. Se creará con datos iniciales.")
        # Aseguramos que los datos iniciales crudos también tengan los cálculos
        d_ventas.ventas = enriquecer_ventas(d_ventas.ventas)
        guardar_cambios()