import env
import psycopg2

USER = env.USER
PASSWORD = env.PASSWORD


def get_all_stations(connection):
    cur = connection.cursor()
    cur.execute("SELECT gps from stations;")
    items = cur.fetchall()
    data = {}
    for i in range(len(items)):
        data[i] = ({"gps": items[i][0]})
    return data


def station_exists(connection, gps: str, serial_number: int) -> bool:
    cur = connection.cursor()
    cur.execute("SELECT * from stations WHERE gps= %s and serial_number = %s ;",
                (gps, serial_number,), )
    if len(cur.fetchall()) == 1:
        return True
    return False


def add_stations(connection, gps: str, serial_number: int):
    cur = connection.cursor()
    cur.execute("INSERT INTO stations(gps, serial_number) VALUES (%s, %s)",
                (gps, serial_number,), )
    connection.commit()


def valid_input(connection, gps: str, serial_number: int):
    cur = connection.cursor()
    cur.execute(
        "SELECT serial_number from serial_numbers WHERE serial_number = %s", (serial_number,))
    if len(cur.fetchall()) != 1:
        return False
    return True


def update_weather(connection, gps: str, serial_number: int, time: int, data):
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO data(gps, serial_number,time, temperature , humidity , pressure , wind_speed , wind_direction , rain) VALUES (%s %s %s %s %s %s %s %s);",
        (gps, serial_number, time, data["temperature"], data["humidity"], data["pressure"], data["wind_speed"], data["wind_direction"], data["rain"],))
    con.commit()


con = psycopg2.connect(
    database="weatherydb", user=USER, password=PASSWORD, host="localhost", port=5432
)
print(get_all_stations(con))
