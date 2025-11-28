import pandas as pd

# ==========================================
# INVENTARIO INICIAL
# ==========================================
inventario = pd.DataFrame({
    "Ingrediente": [
        "Pan hamburguesa","Pan perro","Carne hamburguesa","Tomate","Lechuga","Cebolla","Pepinillos",
        "Papa","Aceite","Sal","Salsas","Gaseosa 350ml","Salchicha","Nugget","Tortilla harina","Pollo pechuga",
        "Crutones","Queso loncha","Frijol cocido","Arroz","Mayonesa"
    ],
    "Stock": [
        200, 100, 150, 3000, 2500, 2000, 800,
        20000, 5000, 2000, 3000, 80, 120, 200, 150, 8000,
        1000, 300, 5000, 6000, 2000
    ],
    "Unidad": [
        "unid","unid","unid","g","g","g","g",
        "g","ml","g","ml","unid","unid","unid","unid","g",
        "g","unid","g","g","ml"
    ]
})