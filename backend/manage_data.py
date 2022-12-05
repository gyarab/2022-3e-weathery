import env
from datetime import datetime
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


def get_latest_data(connection, gps: str):
    cur = connection.cursor()
    cur.execute(
        "SELECT temperature, humidity, pressure, wind_speed, wind_direction, rain, time from data WHERE gps=%s order by time DESC",
        (gps,))
    data = cur.fetchall()[0]
    return {"temperature": data[0], "humidity": data[1], "pressure": data[2], "wind_speed": data[3],
            "wind_direction": data[4], "rain": data[5]}


def get_between_dates(connection, gps: str, date_from: str, date_to: str):
    cur = connection.cursor()
    cur.execute("SELECT time, temperature, humidity, pressure, wind_speed, wind_direction, rain from data WHERE gps=%s and time BETWEEN %s AND %s", (gps, date_from, date_to,))
    items = cur.fetchall()
    data = {"data": []}
    for i in items:
        data["data"].append({"time": str(i[0]), "temperature": i[1], "humidity": i[2], "pressure": i[3], "wind_speed": i[4],
                             "wind_direction": i[5], "rain": i[6]})
    return data


def get_all_data(connection, gps: str, from_date: int, to_date: int):
    cur = connection.cursor()
    cur.execute(
        "SELECT temperature, humidity, pressure, wind_speed, wind_direction, rain ,time FROM data WHERE gps = %s and time > %s and time < %s",
        (gps, from_date, to_date,))
    items = cur.fetchall()
    data = {}
    for i in range(len(items)):
        data[i] = {"temperature": items[i][0], "humidity": items[i][1], "pressure": items[i][2],
                   "wind_speed": items[i][3], "wind_direction": items[i][4], "rain": items[i][5], "time": items[i][6]}
    return data


def station_exists(connection, gps: str) -> bool:
    cur = connection.cursor()
    cur.execute("SELECT gps from stations WHERE gps= %s;",
                (gps,), )
    if len(cur.fetchall()) == 1:
        return True
    return False


def add_stations(connection, gps: str, serial_number: int):
    cur = connection.cursor()
    cur.execute("INSERT INTO stations(gps, serial_number) VALUES (%s, %s)",
                (gps, serial_number,), )
    connection.commit()


def valid_input(connection, serial_number: int):
    cur = connection.cursor()
    cur.execute(
        "SELECT serial_number from serial_numbers WHERE serial_number = %s", (serial_number,))
    if len(cur.fetchall()) != 1:
        return False
    return True


def valid_date(date: str) -> bool:
    format1 = '%d-%m-%Y %H:%M:%S'
    format2 = '%d-%m-%Y'
    if len(date) > 10:
        try:
            datetime.strptime(date, format1)
            return True
        except ValueError:
            return False
    else:
        try:
            datetime.strptime(date, format2)
            return True
        except ValueError:
            return False


def update_weather(connection, gps: str, time: str, data):
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO data(gps, time, temperature , humidity , pressure , wind_speed , wind_direction , rain) VALUES (%s,  %s ,%s ,%s ,%s ,%s ,%s, %s);",
        (gps, time, data["temperature"], data["humidity"], data["pressure"], data["wind_speed"], data["wind_direction"],
         data["rain"],))
    con.commit()


# debug only
def post_data(con):
    format = '%d-%m-%Y %H:%M:%S'
    for i in range(15):
        data = {"temperature": i, "humidity": i * 5, "pressure": i * 1000, "wind_speed": i * 2, "wind_direction": "N",
                "rain": i}
        update_weather(con, "21.123456 -46.123456",
                       datetime.strftime(datetime.now(), format), data)
