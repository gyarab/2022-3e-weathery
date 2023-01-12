import env
import psycopg2

USER = env.DB_USER
PASSWORD = env.DB_PASSWORD
DBNAME = env.DB_NAME
con = psycopg2.connect(
    database=DBNAME, user=USER, password=PASSWORD, host="localhost", port=5432
)
cur = con.cursor()
cur.execute("SET timezone='UTC';")
cur.execute(
    "CREATE TABLE if not exists data (gps TEXT, time TIMESTAMP, temperature FLOAT, humidity FLOAT, pressure FLOAT, wind_speed FLOAT, wind_direction TEXT, rain FLOAT);"
)
cur.execute("CREATE TABLE if not exists stations (gps TEXT, serial_number INT);")

cur.execute("CREATE TABLE if not exists serial_numbers (serial_number INT);")

con.commit()
