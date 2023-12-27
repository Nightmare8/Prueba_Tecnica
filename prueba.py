import psycopg2
from psycopg2 import OperationalError
#Insert values


# INSERT INTO Market (ID_Mercado, nombre) VALUES ('ID1', 'Falabella');
# INSERT INTO Product (SKU, Ean, nombre, ID_Mercado) 
# VALUES ('SKU1', 'Ean1', 'Product1', 'ID1');
# INSERT INTO Product (SKU, Ean, nombre, ID_Mercado) 
# VALUES ('SKU2', 'Ean1', 'Product2', 'ID1');
# INSERT INTO Price (normal_price, precio_descuento, activo, fecha_creada, SKU) 
# VALUES (10.00, 8.00, true, '2023-01-01', 'SKU1');
# INSERT INTO Price (normal_price, precio_descuento, activo, fecha_creada, SKU) 
# VALUES (12.00, 8.00, true, '2023-03-01', 'SKU2');
# INSERT INTO Price (normal_price, precio_descuento, activo, fecha_creada, SKU) 
# VALUES (12.00, 9.00, true, '2023-03-01', 'SKU2');
# INSERT INTO Price (normal_price, precio_descuento, activo, fecha_creada, SKU) 
# VALUES (10.00, 2.00, true, '2023-02-01', 'SKU2');

datos = [
    "INSERT INTO Market (ID_Market, Name) VALUES ('ID1', 'Falabella');",
    "INSERT INTO Market (ID_Market, Name) VALUES ('ID2', 'Paris');",
    "INSERT INTO Product (SKU, Ean, Name, ID_Market) VALUES ('SKU1', 'Ean1', 'Product1', 'ID1');",
    "INSERT INTO Product (SKU, Ean, Name, ID_Market) VALUES ('SKU2', 'Ean2', 'Product2', 'ID1');",
    "INSERT INTO Product (SKU, Ean, Name, ID_Market) VALUES ('SKU3', 'Ean2', 'Product3', 'ID1');",
    "INSERT INTO Product (SKU, Ean, Name, ID_Market) VALUES ('SKU4', 'Ean1', 'Product4', 'ID2');",
    "INSERT INTO Product (SKU, Ean, Name, ID_Market) VALUES ('SKU5', 'Ean3', 'Product5', 'ID2');",
    "INSERT INTO Product (SKU, Ean, Name, ID_Market) VALUES ('SKU6', 'Ean3', 'Product6', 'ID2');",
    "INSERT INTO Price (normal_price, discount_price, active, create_date, SKU) VALUES (10.00, 8.00, true, '2023-01-01', 'SKU1');",
    "INSERT INTO Price (normal_price, discount_price, active, create_date, SKU) VALUES (12.00, 8.00, true, '2023-03-01', 'SKU2');",
    "INSERT INTO Price (normal_price, discount_price, active, create_date, SKU) VALUES (12.00, 8.00, true, '2023-03-01', 'SKU3');",
    "INSERT INTO Price (normal_price, discount_price, active, create_date, SKU) VALUES (22.00, 8.00, true, '2023-03-01', 'SKU4');",
    "INSERT INTO Price (normal_price, discount_price, active, create_date, SKU) VALUES (42.00, 8.00, true, '2023-03-01', 'SKU5');",
    "INSERT INTO Price (normal_price, discount_price, active, create_date, SKU) VALUES (10.00, 8.00, true, '2023-03-01', 'SKU6');",
]

queryEnunciado = "SELECT Product.SKU, Product.Name, Product.Ean, Market.Name, MIN(normal_price-discount_price) as Precio_final FROM Product INNER JOIN Market ON Product.ID_Market = Market.ID_Market INNER JOIN Price ON Product.SKU = Price.SKU WHERE Price.active = true GROUP BY Product.SKU, Market.name ORDER BY MAX(Price.create_date) DESC;"

#El nombre de la base de datos es prueba
def crear_tablas(conn):
    try:
        cursor = conn.cursor()
        postgreSQL_select_Query = "CREATE TABLE Market (ID_Market VARCHAR(50) PRIMARY KEY, Name VARCHAR(50));"
        cursor.execute(postgreSQL_select_Query)
        postgreSQL_select_Query = "CREATE TABLE Product (SKU VARCHAR(50) PRIMARY KEY, Ean VARCHAR(50), Name VARCHAR(50), ID_Market VARCHAR(50), FOREIGN KEY (ID_Market) REFERENCES Market(ID_Market));"
        cursor.execute(postgreSQL_select_Query)
        postgreSQL_select_Query = "CREATE TABLE Price (normal_price FLOAT, discount_price FLOAT, active BOOLEAN, create_date DATE, SKU VARCHAR(50), FOREIGN KEY (SKU) REFERENCES Product(SKU));"
        cursor.execute(postgreSQL_select_Query)
        conn.commit()
        print ("Tabla creada exitosamente")
    except (Exception, psycopg2.Error) as error:
        print("Error creando la tabla", error)
        conn.rollback()


def borrar_tabla (conn, table):
    try:
        cursor = conn.cursor()
        postgreSQL_select_Query = "DROP TABLE " + table + " CASCADE;"
        cursor.execute(postgreSQL_select_Query)
        print ("Tabla borrada exitosamente")
    except (Exception, psycopg2.Error) as error:
        print("Error borrando la tabla", error)
        conn.rollback()
def borrar_tablas(conn):
    try:
        cursor = conn.cursor()
        postgreSQL_select_Query = "DROP TABLE Price;"
        cursor.execute(postgreSQL_select_Query)
        postgreSQL_select_Query = "DROP TABLE Product;"
        cursor.execute(postgreSQL_select_Query)
        postgreSQL_select_Query = "DROP TABLE Market;"
        cursor.execute(postgreSQL_select_Query)
        print ("Tabla borrada exitosamente")
    except (Exception, psycopg2.Error) as error:
        print("Error borrando la tabla", error)
        conn.rollback() 
def borrar_datos(conn, table):
    try:
        cursor = conn.cursor()
        postgreSQL_select_Query = "delete from " + table
        cursor.execute(postgreSQL_select_Query)
        conn.commit()
        print ("Datos borrados exitosamente")
    except (Exception, psycopg2.Error) as error:
        print("Error borrando datos de la tabla", error)
        conn.rollback()

def agregar_datos(conn):
    try:
        cursor = conn.cursor()
        for dato in datos:
            cursor.execute(dato)
        conn.commit()
        print ("Datos agregados exitosamente")
    except (Exception, psycopg2.Error) as error:
        print("Error agregando datos a la tabla", error)
        conn.rollback()

#La funcion pedida en el enunciado de transformar los datos con el formato pedido
def transformar_datos(datos, query):
    response = []
    #Diccionario para agrupar por EAN
    dict = {}
    for dato in datos:
        #Desempaquetar la tupla
        sku, name, ean, market, precio = dato
        #Si el ean no esta en el diccionario, lo agregamos
        if ean not in dict:
            dict[ean] = {
                "nombre_producto": name,
                "datos_query": query,
                "markets": [market],
                "rango_precios": (precio, precio)
            }  
        else:
            #Si el ean esta en el diccionario, agregamos el market
            if market not in dict[ean]["markets"]:
                dict[ean]["markets"].append(market)
            #Actualizamos el rango de precios (mayor precio, menor precio)
            #Si el precio actual es mayor al maximo, lo actualizamos
            if precio > dict[ean]["rango_precios"][0]:
                dict[ean]["rango_precios"] = (precio, dict[ean]["rango_precios"][1])
            elif precio < dict[ean]["rango_precios"][1]:
                dict[ean]["rango_precios"] = (dict[ean]["rango_precios"][0], precio)
                
    response.append(dict)
    return response

def consultar_datos(conn):
    try:
        cursor = conn.cursor()
        #Usamos la query que se define en el documento
        postgreSQL_select_Query = queryEnunciado
        cursor.execute(postgreSQL_select_Query)
        prueba_records = cursor.fetchall() 
        print ("Datos consultados exitosamente")
        #Transformamos los datos con el formato pedido
        prueba_records = transformar_datos(prueba_records, postgreSQL_select_Query)
        print ("Datos transformados exitosamente")
        print ("Datos: ", prueba_records)
    except (Exception, psycopg2.Error) as error:
        print("Error consultando datos de la tabla", error)


conn = None
try:
    conn = psycopg2.connect(
        dbname='prueba',
        user='postgres',
        password='0201',
        host='localhost',
        port='5432')
    print("Database connected successfully")
    borrar_tablas(conn)
    crear_tablas(conn)
    agregar_datos(conn)
    consultar_datos(conn)
    
except OperationalError as e:
    print("I am unable to connect to the database")
    print(e)
finally:
    if conn is not None:
        conn.close()


