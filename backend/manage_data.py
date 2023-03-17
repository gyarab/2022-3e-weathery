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
    increment_map = {
        1: timedelta(seconds=300),
        2: timedelta(seconds=1800),
        3: timedelta(hours=1),
        4: timedelta(days=1),
        5: timedelta(weeks=1),
        6: timedelta(weeks=2),
        7: timedelta(weeks=4),
    }

    increment = increment_map[avg_type]
    while d_from <= d_to:
        data["data"].append(
            execute_between_dates(connection, gps, d_from, d_from + increment)
        )
        d_from += increment
    return data


def execute_between_dates(connection, gps: str, d_from: datetime, to: datetime) -> dict:
    format = "%d-%m-%Y %H:%M:%S"
    cur = connection.cursor()
    cur.execute(
        "select count(*), min(time), avg(temperature), avg(humidity), avg(pressure), avg(wind_speed),MODE() WITHIN GROUP (ORDER BY wind_direction), avg(rain) from data where id = %s and time between %s and %s group by id",
        (
            get_id_by_gps(connection, gps),
            d_from,
            to,
        ),
    )
    items = cur.fetchall()
    if len(items) == 0:
        return {
            "time": str(datetime.strftime(d_from, format)),
            "temperature": 0,
            "humidity": 0,
            "pressure": 0,
            "wind_speed": 0,
            "wind_direction": "",
            "rain": 0,
            "average_of": 0,
        }
    return {
        "time": str(datetime.strftime(items[0][1], format)),
        "temperature": items[0][2],
        "humidity": items[0][3],
        "pressure": items[0][4],
        "wind_speed": items[0][5],
        "wind_direction": items[0][6],
        "rain": items[0][7],
        "average_of": items[0][0],
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
    cur.execute(
        "SELECT id from serial_numbers WHERE id = %s",
        (id,),
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


def create_order(connection, customer_data: dict) -> None:
    cur = connection.cursor()
    cur.execute(
        "INSERT into orders(id, order_state, email, name, country, state, city, street, postal_code, date, stripe_json) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s);",
        (
            customer_data["id"],
            "pending",
            customer_data["email"],
            customer_data["name"],
            customer_data["address"]["country"],
            customer_data["address"]["state"],
            customer_data["address"]["city"],
            customer_data["address"]["line1"],
            customer_data["address"]["postal_code"],
            customer_data["date"],
            customer_data["stripe_json"],
        ),
    )
    connection.commit()


def update_order_state(connection, id: int, order_state: str) -> None:
    cur = connection.cursor()
    cur.execute(
        "update orders set order_state = %s where id = %s",
        (
            order_state,
            id,
        ),
    )
    connection.commit()


def order_exists(connection, id: int) -> bool:
    cur = connection.cursor()
    cur.execute("select id from orders where id = %s", (id,))
    items = cur.fetchall()
    if len(items) > 0:
        return True
    return False


def get_order_details(connection, id: int) -> dict:
    cur = connection.cursor()
    cur.execute(
        "select id, order_state, email, name, country, state, city, street, postal_code, date from orders where id = %s",
        (id,),
    )
    data = cur.fetchall()
    if len(data) < 1:
        return {"message": "order does not exist"}
    items = data[0]
    details = {
        "id": items[0],
        "order_state": items[1],
        "email": items[2],
        "name": items[3],
        "country": items[4],
        "state": items[5],
        "city": items[6],
        "street": items[7],
        "postal_code": items[8],
        "date": items[9],
    }
    return {"message": "ok", "data": details}


def get_all_orders(connection) -> dict:
    cur = connection.cursor()
    cur.execute("select id from orders")
    items = cur.fetchall()
    orders = []
    for x in items:
        orders.append({"id": x[0]})
    return {"message": "ok", "orders": orders}


def get_home_page_data(connection) -> dict:
    result = {
        "min-temp": get_min_temp(connection),
        "max-temp": get_max_temp(connection),
        "avg-temp": get_avg_temp(connection),
        "min-rain": get_min_rain(connection),
        "max-rain": get_max_rain(connection),
        "avg-rain": get_avg_rain(connection),
    }
    return result


def get_min_temp(connection) -> dict:
    cur = connection.cursor()
    cur.execute(
        "select min(temperature), date_trunc('YEAR', time ) as trunc from data group by trunc order by trunc;"
    )
    result = {}
    items = cur.fetchall()
    for i in items:
        result[i[1][:4]] = i[0]
    return result


def get_avg_temp(connection) -> dict:
    cur = connection.cursor()
    cur.execute(
        "select avg(temperature), date_trunc('YEAR', time ) as trunc from data group by trunc order by trunc;"
    )
    result = {}
    items = cur.fetchall()
    for i in items:
        result[i[1][:4]] = i[0]
    return result


def get_max_temp(connection) -> dict:
    cur = connection.cursor()
    cur.execute(
        "select max(temperature), date_trunc('YEAR', time ) as trunc from data group by trunc order by trunc;"
    )
    result = {}
    items = cur.fetchall()
    for i in items:
        result[i[1][:4]] = i[0]
    return result


def get_min_rain(connection) -> dict:
    cur = connection.cursor()
    cur.execute(
        "select min(rain), date_trunc('YEAR', time ) as trunc from data group by trunc order by trunc;"
    )
    result = {}
    items = cur.fetchall()
    for i in items:
        result[i[1][:4]] = i[0]
    return result


def get_avg_rain(connection) -> dict:
    cur = connection.cursor()
    cur.execute(
        "select avg(rain), date_trunc('YEAR', time ) as trunc from data group by trunc order by trunc;"
    )
    result = {}
    items = cur.fetchall()
    for i in items:
        result[i[1][:4]] = i[0]
    return result


def get_max_rain(connection) -> dict:
    cur = connection.cursor()
    cur.execute(
        "select max(rain), date_trunc('YEAR', time ) as trunc from data group by trunc order by trunc;"
    )
    result = {}
    items = cur.fetchall()
    for i in items:
        result[i[1][:4]] = i[0]
    return result


def get_email(connection, id) -> str:
    cur = connection.cursor()
    cur.execute("select email from orders where id = %s", (id,))
    return cur.fetchall()[0][0]


def get_admin_emails(connection) -> list:
    cur = connection.cursor()
    cur.execute("select email from super_users")
    emails = []
    for x in cur.fetchall():
        emails.append(x[0])
    return emails


def user_exists(connection, name: str) -> bool:
    cur = connection.cursor()
    cur.execute("select name from super_users where name = %s", (name,))
    if len(cur.fetchall()) > 0:
        return True
    return False


def get_password(connection, name: str) -> str:
    cur = connection.cursor()
    cur.execute("select password from super_users where name = %s", (name,))
    return cur.fetchall()[0][0]
