import env
import psycopg2

USER = env.USER
PASSWORD = env.PASSWORD

con = psycopg2.connect(
    database="weatherydb", user=USER, password=PASSWORD, host="localhost", port=5432
)
cur = con.cursor()

cur.execute("CREATE TABLE stations (gps TEXT, serial_number INT);")
cur.execute(
    "CREATE TABLE data (gps TEXT, serial_number INT, time INT, temperature INT, humidity INT, pressure INT, wind_speed INT, wind_direction TEXT, rain INT);"
)
cur.execute("CREATE TABLE serial_numbers (serial_number INT);")

con.commit()
