import env
from datetime import datetime, timedelta

USER = env.USER
PASSWORD = env.PASSWORD


def get_all_stations(connection):
    cur = connection.cursor()
    cur.execute("SELECT gps from stations;")
    items = cur.fetchall()
    data = {}
    for i in range(len(items)):
        data[i] = {"gps": items[i][0]}
    return data


def get_latest_data(connection, gps: str):
    cur = connection.cursor()
    cur.execute(
        "SELECT temperature, humidity, pressure, wind_speed, wind_direction, rain, time from data WHERE gps=%s order by time DESC",
        (gps,),
    )
    data = cur.fetchall()[0]
    return {
        "temperature": data[0],
        "humidity": data[1],
        "pressure": data[2],
        "wind_speed": data[3],
        "wind_direction": data[4],
        "rain": data[5],
    }


def get_between_dates(
    connection, gps: str, avg_type: int, date_from: str, date_to: str
):
    format = "%d-%m-%Y %H:%M:%S"
    d_from = datetime.strptime(date_from, format)
    d_to = datetime.strptime(date_to, format)
    data = {"data": []}
    match avg_type:
        case 0:
            delta = d_to - d_from
            for i in range((delta.seconds // 3600) + 1):
                to = d_to - timedelta(hours=(delta.seconds // 3600) - i)
                data["data"].append(execute_between_dates(connection, gps, d_from, to))
                d_from += timedelta(hours=1)
        case 1:
            delta = d_to - d_from
            for i in range(delta.days + 1):
                to = d_to - timedelta(delta.days - i)
                data["data"].append(execute_between_dates(connection, gps, d_from, to))
                d_from += timedelta(days=1)
        case 2:
            delta = d_to - d_from
            for i in range((delta.days // 7) + 1):
                to = d_to - timedelta((delta.days // 7) - i)
                data["data"].append(execute_between_dates(connection, gps, d_from, to))
                d_from += timedelta(weeks=1)

    return data


def execute_between_dates(connection, gps, d_from, to):
    format = "%d-%m-%Y %H:%M:%S"
    cur = connection.cursor()
    cur.execute(
        "SELECT time, temperature, humidity, pressure, wind_speed, wind_direction, rain from data WHERE gps=%s and time BETWEEN %s AND %s",
        (
            gps,
            d_from,
            to,
        ),
    )
    items = cur.fetchall()
    temperature, humidity, pressure, wind_speed, rain = 0, 0, 0, 0, 0
    wind_direction = ""
    for i in items:
        temperature += i[1]
        humidity += i[2]
        pressure += i[3]
        wind_speed += i[4]
        wind_direction += i[5]
        rain += i[6]
    avg = len(items) if len(items) > 0 else 1
    data = {
        "time": str(datetime.strftime(d_from, format)),
        "temperature": temperature / avg,
        "humidity": humidity / avg,
        "pressure": pressure / avg,
        "wind_speed": wind_speed / avg,
        "wind_direction": max(wind_direction, key=wind_direction.count),
        "rain": rain / avg,
        "average_of": avg,
    }
    return data


def get_all_data(connection, gps: str, from_date: int, to_date: int):
    cur = connection.cursor()
    cur.execute(
        "SELECT temperature, humidity, pressure, wind_speed, wind_direction, rain ,time FROM data WHERE gps = %s and time > %s and time < %s",
        (
            gps,
            from_date,
            to_date,
        ),
    )
    items = cur.fetchall()
    data = {}
    for i in range(len(items)):
        data[i] = {
            "temperature": items[i][0],
            "humidity": items[i][1],
            "pressure": items[i][2],
            "wind_speed": items[i][3],
            "wind_direction": items[i][4],
            "rain": items[i][5],
            "time": items[i][6],
        }
    return data


def station_exists(connection, gps: str) -> bool:
    cur = connection.cursor()
    cur.execute(
        "SELECT gps from stations WHERE gps= %s;",
        (gps,),
    )
    if len(cur.fetchall()) == 1:
        return True
    return False


def add_stations(connection, gps: str, serial_number: int):
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO stations(gps, serial_number) VALUES (%s, %s)",
        (
            gps,
            serial_number,
        ),
    )
    connection.commit()


def valid_input(connection, serial_number: int):
    cur = connection.cursor()
    cur.execute(
        "SELECT serial_number from serial_numbers WHERE serial_number = %s",
        (serial_number,),
    )
    if len(cur.fetchall()) != 1:
        return False
    return True


def valid_date(date: str) -> bool:
    format1 = "%d-%m-%Y %H:%M:%S"
    format2 = "%d-%m-%Y"
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
        (
            gps,
            time,
            data["temperature"],
            data["humidity"],
            data["pressure"],
            data["wind_speed"],
            data["wind_direction"],
            data["rain"],
        ),
    )
    connection.commit()
