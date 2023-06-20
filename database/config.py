import psycopg2

# conn = psycopg2.connect("dbname=crud user= password=")
import psycopg2
conn = None
try:
    conn = psycopg2.connect("dbname=crud user=postgres")
    # conn = psycopg2.connect(
    #     host="localhost",
    #     port="5432",
    #     database="crud",
    #     user="",
    #     password=""
    # )
    
    print("La conexion está funcionando")

except psycopg2.OperationalError as e:
    print("Error de conexión a la base de datos:", e)

