from datetime import datetime, timedelta


def get_id_by_gps(connection, gps: str) -> int:
    cur = connection.cursor()
    cur.execute("SELECT id from stations where gps=%s", (gps,))
    return cur.fetchall()[0][0]


def get_all_stations(connection) -> dict:
    cur = connection.cursor()
    cur.execute("SELECT gps from stations;")
    items = cur.fetchall()
    data = {"message": "ok", "station": []}
    for i in range(len(items)):
        data["station"].append({"gps": items[i][0]})
    return data


def get_latest_data(connection, gps: str) -> dict:
    cur = connection.cursor()
    format = "%d-%m-%Y %H:%M:%S"
    cur.execute(
        "SELECT temperature, humidity, pressure, wind_speed, wind_direction, rain, time from data WHERE id=%s order by time DESC",
        (get_id_by_gps(connection, gps),),
    )
    data = cur.fetchall()
    if len(data) <= 0:
        return {"message": "no data found"}
    data = data[0]
    return {
        "message": "ok",
        "time": str(datetime.strftime(data[6], format)),
        "temperature": data[0],
        "humidity": data[1],
        "pressure": data[2],
        "wind_speed": data[3],
        "wind_direction": data[4],
        "rain": data[5],
    }


def get_between_dates(
    connection, gps: str, avg_type: int, date_from: str, date_to: str
) -> dict:
    format = "%d-%m-%Y %H:%M:%S"
    d_from = datetime.strptime(date_from, format)
    d_to = datetime.strptime(date_to, format)
    data = {"message": "ok", "data": []}
    delta = d_to - d_from
    match avg_type:
        case 1:
            for i in range((int(delta.total_seconds()) // 300) + 1):
                data["data"].append(
                    execute_between_dates(
                        connection, gps, d_from, d_from + timedelta(seconds=300)
                    )
                )
                d_from += timedelta(seconds=300)
        case 2:
            for i in range((int(delta.total_seconds()) // 1800) + 1):
                data["data"].append(
                    execute_between_dates(
                        connection, gps, d_from, d_from + timedelta(seconds=1800)
                    )
                )
                d_from += timedelta(seconds=1800)
        case 3:
            for i in range((int(delta.total_seconds()) // 3600) + 1):
                data["data"].append(
                    execute_between_dates(
                        connection, gps, d_from, d_from + timedelta(hours=1)
                    )
                )
                d_from += timedelta(hours=1)
        case 4:
            for i in range((int(delta.total_seconds()) // 86400) + 1):
                data["data"].append(
                    execute_between_dates(
                        connection, gps, d_from, d_from + timedelta(days=1)
                    )
                )
                d_from += timedelta(days=1)
        case 5:
            for i in range((int(delta.total_seconds()) // 604800) + 1):
                data["data"].append(
                    execute_between_dates(
                        connection, gps, d_from, d_from + timedelta(weeks=1)
                    )
                )
                d_from += timedelta(weeks=1)
    return data


def execute_between_dates(connection, gps: str, d_from: datetime, to: datetime) -> dict:
    format = "%d-%m-%Y %H:%M:%S"
    cur = connection.cursor()
    cur.execute(
        "SELECT time, temperature, humidity, pressure, wind_speed, wind_direction, rain from data WHERE id=%s and time BETWEEN %s AND %s",
        (
            get_id_by_gps(connection, gps),
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
    avg = len(items)
    if avg > 0:
        return {
            "time": str(datetime.strftime(d_from, format)),
            "temperature": temperature / avg,
            "humidity": humidity / avg,
            "pressure": pressure / avg,
            "wind_speed": wind_speed / avg,
            "wind_direction": max(wind_direction, key=wind_direction.count),
            "rain": rain / avg,
            "average_of": avg,
        }
    return {
        "time": str(datetime.strftime(d_from, format)),
        "temperature": 0,
        "humidity": 0,
        "pressure": 0,
        "wind_speed": 0,
        "wind_direction": "",
        "average_of": 0,
    }


def station_exists(connection, gps: str) -> bool:
    cur = connection.cursor()
    cur.execute(
        "SELECT gps from stations WHERE gps= %s;",
        (gps,),
    )
    if len(cur.fetchall()) == 1:
        return True
    return False


def id_exists(connection, id: int) -> bool:
    cur = connection.cursor()
    cur.execute("SELECT id from stations where id= %s;", (id,))
    if len(cur.fetchall()) == 1:
        return True
    return False


def update_station(connection, id: int, gps: str) -> None:
    cur = connection.cursor()
    cur.execute(
        "UPDATE stations SET gps = %s WHERE id = %s",
        (
            gps,
            id,
        ),
    )
    connection.commit()


def add_stations(connection, gps: str, id: int) -> None:
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO stations(gps, id) VALUES (%s, %s)",
        (
            gps,
            id,
        ),
    )
    connection.commit()


def valid_input(connection, id: int) -> bool:
    cur = connection.cursor()
    cur2 = connection.cursor()
    cur.execute(
        "SELECT id from serial_numbers WHERE id = %s",
        (id,),
    )
    if len(cur.fetchall()) != 1:
        return False
    cur2.execute(
        "select id from stations where id = %s",
        (id,),
    )
    if len(cur2.fetchall()) > 0:
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


def update_weather(connection, id: int, time: str, data) -> None:
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO data(id, time, temperature , humidity , pressure , wind_speed , wind_direction , rain) VALUES (%s,  %s ,%s ,%s ,%s ,%s ,%s, %s);",
        (
            id,
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
