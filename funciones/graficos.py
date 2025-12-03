import matplotlib
# ⚠️ ESTA LÍNEA ES OBLIGATORIA PARA EVITAR EL CUELGUE EN SERVIDORES/STREAMLIT
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import data.ventas as d_ventas
import data.inventario as d_inv

def generar_grafico_avanzado(solicitud: str):
    """
    Genera gráficos de ventas o inventario.
    Entrada esperada: una cadena con 'tipo,metrica'. Ej: 'barras,inventario' o 'pastel,productos'.
    """
    # 1. Limpiar la figura actual para evitar superposiciones de gráficos viejos
    plt.clf() 
    plt.close() 

    ventas = d_ventas.ventas
    inventario = d_inv.inventario
    
    # Manejo de errores si la entrada del agente no es perfecta
    try:
        parts = solicitud.split(",")
        if len(parts) >= 2:
            tipo = parts[0].strip().lower()
            metrica = parts[1].strip().lower()
        else:
            # Si el agente solo manda una palabra, asumimos valores por defecto
            tipo = "barras"
            metrica = solicitud.strip().lower()
    except Exception as e:
        return f"Error interpretando solicitud: {str(e)}. Intenta: 'tipo,metrica'"

    plt.figure(figsize=(10, 6))
    titulo = ""
    nombre_archivo = "reporte_grafico.png"
    mensaje_salida = ""

    try:
        if "inventario" in metrica:
            if inventario.empty: return "El inventario está vacío, no se puede graficar."
            # Tomar solo los top 10 para que el gráfico no sea gigante
            df = inventario.sort_values(by="Stock", ascending=False).head(15)
            plt.bar(df["Ingrediente"], df["Stock"], color='orange')
            titulo = "Top 15 Ingredientes en Stock"
            plt.xticks(rotation=45, ha='right') # Rotar nombres para que se lean
        
        elif "producto" in metrica:
            if ventas.empty: return "No hay ventas registradas para graficar."
            df = ventas.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False)
            if df.empty: return "No hay datos agrupables."
            df.plot(kind='bar' if 'barra' in tipo else 'pie', autopct='%1.1f%%' if 'pastel' in tipo else None)
            titulo = "Ventas por Producto"
            if 'barra' in tipo: plt.xticks(rotation=45, ha='right')

        elif "ganancia" in metrica:
            if ventas.empty: return "No hay ventas registradas."
            df = ventas.assign(Dia=ventas["Fecha"].dt.date).groupby("Dia")["Ganancia"].sum()
            df.plot(kind='line', marker='o', color='green')
            titulo = "Ganancias por Día"
            plt.grid(True)

        else:
            # Por defecto: Ingresos por día
            if ventas.empty: return "No hay ventas registradas."
            df = ventas.assign(Dia=ventas["Fecha"].dt.date).groupby("Dia")["Total"].sum()
            df.plot(kind='bar', color='blue')
            titulo = "Ingresos Totales por Día"
            plt.xticks(rotation=45)

        plt.title(titulo)
        plt.tight_layout() # Ajusta los márgenes automáticamente
        
        # Guardar imagen
        plt.savefig(nombre_archivo)
        mensaje_salida = f"Gráfico generado exitosamente: {nombre_archivo}. Muestra este archivo al usuario."

    except Exception as e:
        mensaje_salida = f"Error generando el gráfico con matplotlib: {str(e)}"
    finally:
        # Cerrar la figura para liberar memoria
        plt.close()

    return mensaje_salida