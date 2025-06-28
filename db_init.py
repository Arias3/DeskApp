import mysql.connector
from mysql.connector import errorcode

DB_NAME = "heladeria"

TABLES = {
    "products": (
        "CREATE TABLE IF NOT EXISTS products ("
        "  id INT AUTO_INCREMENT PRIMARY KEY,"
        "  code VARCHAR(20) NOT NULL UNIQUE,"
        "  name VARCHAR(100) NOT NULL,"
        "  cost DECIMAL(10,2) NOT NULL,"
        "  price DECIMAL(10,2) NOT NULL,"
        "  profitability DECIMAL(10,2),"
        "  stock DECIMAL(10,2),"
        "  barcode VARCHAR(50),"
        "  unit VARCHAR(20),"
        "  image_url VARCHAR(255),"
        "  flavor_count INT,"
        "  description TEXT,"
        "  categoria TEXT"
        ") ENGINE=InnoDB;"
    ),
    "flavors": (
        "CREATE TABLE IF NOT EXISTS flavors ("
        "  id INT AUTO_INCREMENT PRIMARY KEY,"
        "  name VARCHAR(50) NOT NULL,"
        "  status ENUM('Disponible', 'No Disponible') DEFAULT 'Disponible'"
        ") ENGINE=InnoDB"
    ),
    "tables": (
        "CREATE TABLE IF NOT EXISTS tables ("
        "  id INT AUTO_INCREMENT PRIMARY KEY,"
        "  name VARCHAR(20) NOT NULL,"
        "  status ENUM('Disponible', 'Ocupada') DEFAULT 'Disponible'"
        ") ENGINE=InnoDB"
    ),
    "staff": (
        "CREATE TABLE IF NOT EXISTS staff ("
        "  id BIGINT PRIMARY KEY,"
        "  name VARCHAR(100) NOT NULL,"
        "  role VARCHAR(50) NOT NULL"
        ") ENGINE=InnoDB"
    ),
    "daily_closures": (
        "CREATE TABLE IF NOT EXISTS daily_closures ("
        "  id INT AUTO_INCREMENT PRIMARY KEY,"
        "  date DATE NOT NULL,"
        "  time TIME NOT NULL,"
        "  cash DECIMAL(10,2) DEFAULT 0.00,"
        "  electronic DECIMAL(10,2) DEFAULT 0.00,"
        "  declared_total DECIMAL(10,2) DEFAULT 0.00,"
        "  expenses DECIMAL(10,2) DEFAULT 0.00"
        ") ENGINE=InnoDB"
    ),
    "sales": (
        "CREATE TABLE IF NOT EXISTS sales ("
        "  id INT AUTO_INCREMENT PRIMARY KEY,"
        "  table_number INT,"
        "  date DATE NOT NULL,"
        "  time TIME NOT NULL,"
        "  description TEXT,"
        "  total DECIMAL(10,2) NOT NULL,"
        "  type ENUM('Table', 'Takeaway', 'App') NOT NULL,"
        "  seller VARCHAR(100) NOT NULL,"
        "  status ENUM('PAID', 'PENDING', 'PREPARING') DEFAULT 'PENDING'"
        ") ENGINE=InnoDB"
    ),
}


def crear_bd_y_tablas(host, user, password):
    print("Conectando a MySQL...")
    try:
        print("Intentando conectar a MySQL...")
        cnx = mysql.connector.connect(
            host="localhost", user="root", password="Mesapp2025", connection_timeout=5
        )
        print("Conexión exitosa.")
        cursor = cnx.cursor()
        try:
            print(f"Creando base de datos {DB_NAME} si no existe...")
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'"
            )
            print("Base de datos verificada/creada.")
        except mysql.connector.Error as err:
            print(f"Error creando base de datos: {err}")
            raise Exception(f"Error creando base de datos: {err}")
        cnx.database = DB_NAME

        for nombre, ddl in TABLES.items():
            try:
                print(f"Creando tabla {nombre}...")
                cursor.execute(ddl)
                print(f"Tabla {nombre} lista.")
            except mysql.connector.Error as err:
                print(f"Error creando tabla {nombre}: {err.msg}")
                raise Exception(f"Error creando tabla {nombre}: {err.msg}")
        cursor.close()
        cnx.close()
        print("Base de datos y tablas listas.")
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        raise Exception(f"Error de conexión: {err}")


if __name__ == "__main__":
    # Cambia estos valores según tu entorno
    crear_bd_y_tablas(host="localhost", user="root", password="Mesapp2025")
