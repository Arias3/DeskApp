import pandas as pd
import mysql.connector
import numpy as np

# Cargar el archivo Excel
df = pd.read_excel("Productos.xlsx")

# Eliminar duplicados por 'code'
df = df.drop_duplicates(subset='code')

# Reemplazar NaN por None para insertar como NULL en MySQL
df = df.replace({np.nan: None})

# Conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mesapp2025",
    database="heladeria"
)
cursor = conn.cursor()

# Query de inserción
insert_query = """
INSERT INTO products (
    code, name, cost, price, profitability, stock,
    barcode, unit, image_url, flavor_count, description, categoria
) VALUES (
    %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s
)
"""

# Convertir DataFrame a lista de tuplas
product_data = list(df.itertuples(index=False, name=None))


# Insertar datos
cursor.executemany(insert_query, product_data)

# Guardar y cerrar
conn.commit()
cursor.close()
conn.close()

print("✅ Productos insertados correctamente.")
