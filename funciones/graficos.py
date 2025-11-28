import matplotlib.pyplot as plt
import data.ventas as d_ventas
import data.inventario as d_inv

def generar_grafico_avanzado(solicitud: str):
    ventas = d_ventas.ventas
    inventario = d_inv.inventario
    
    try:
        tipo, metrica = [x.strip().lower() for x in solicitud.split(",")]
    except:
        tipo = "barras"
        metrica = "dias"

    plt.figure(figsize=(10, 6))
    titulo = ""
    nombre_archivo = "reporte_grafico.png"

    if "inventario" in metrica:
        if inventario.empty: return "Inventario vacío."
        df = inventario.sort_values(by="Stock", ascending=False)
        plt.bar(df["Ingrediente"], df["Stock"], color='orange')
        titulo = "Stock Inventario"
        plt.xticks(rotation=90)
    
    elif "producto" in metrica:
        if ventas.empty: return "Sin ventas."
        df = ventas.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False)
        df.plot(kind='bar' if tipo!='pastel' else 'pie')
        titulo = "Ventas por Producto"
    
    elif "ganancia" in metrica:
        if ventas.empty: return "Sin ventas."
        df = ventas.assign(Dia=ventas["Fecha"].dt.date).groupby("Dia")["Ganancia"].sum()
        df.plot(kind='line' if 'linea' in tipo else 'bar', color='green')
        titulo = "Ganancias por Día"
    
    else:
        if ventas.empty: return "Sin ventas."
        df = ventas.assign(Dia=ventas["Fecha"].dt.date).groupby("Dia")["Total"].sum()
        df.plot(kind='bar', color='blue')
        titulo = "Ingresos por Día"

    plt.title(titulo)
    plt.tight_layout()
    plt.savefig(nombre_archivo)
    plt.close()
    return f"✅ Gráfico generado: {nombre_archivo} ({titulo})"