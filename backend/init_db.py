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
    "CREATE TABLE if not exists data (gps TEXT not null, time TIMESTAMP not null, temperature FLOAT not null, humidity FLOAT not null, pressure FLOAT not null, wind_speed FLOAT not null, wind_direction TEXT not null, rain FLOAT not null);"
)
cur.execute(
    "CREATE TABLE if not exists stations (gps TEXT not null, serial_number INT not null);"
)

cur.execute(
    "CREATE TABLE if not exists serial_numbers (serial_number INT not null unique);"
)

con.commit()
