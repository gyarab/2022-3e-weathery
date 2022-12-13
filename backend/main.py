import env
from datetime import datetime
import jwt
import psycopg2
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from manage_data import (
    add_stations,
    get_all_stations,
    station_exists,
    update_weather,
    valid_date,
    valid_input,
    get_latest_data,
    get_between_dates,
)
from models import Data, RegisterData

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"

DAY = 86400
MONTH = 2678400

USER = env.USER
PASSWORD = env.PASSWORD

app = FastAPI()
con = psycopg2.connect(
    database="weatherydb", user=USER, password=PASSWORD, host="localhost", port=5432
)


def get_token(req):
    try:
        token = req.headers["Authorization"].split()[1]
        return jwt.decode(token, SECRET_KEY)
    except KeyError:
        return None


def authorized_token(token) -> bool:
    return station_exists(con, token["gps"])


def create_token(gps, serial_number):
    payload = {"gps": gps, "serial_number": serial_number}
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.get("/api/stations")
async def stations():
    return get_all_stations(con)


@app.get("/api/now/{gps}")
async def now(gps: str):
    if not station_exists(con, gps):
        return {"message": "station does not exist"}
    return get_latest_data(con, gps)


# TODO: vrati vsechna namerena data ze stanice s danymi GPS
@app.get("/api/stats/{gps}/{date_from}/{date_to}")
async def stats(gps: str, date_from: str, date_to: str = "now"):
    format = "%d-%m-%Y %H:%M:%S"
    if date_to == "now":
        date_to = str(datetime.strftime(datetime.now(), "%d-%m-%Y")) + " 23:59:59"
    if not valid_date(date_from):
        return {"message": "date is not valid"}
    if not valid_date(date_to):
        return {"message": "date is not valid"}
    if len(date_from) <= 10:
        date_from += " 00:00:00"
    if len(date_to) <= 10:
        date_to += " 23:59:59"
    unix_delta = datetime.timestamp(
        datetime.strptime(date_to, format)
    ) - datetime.timestamp(datetime.strptime(date_from, format))
    if unix_delta <= 0:
        return {"message": "date is not valid"}
    elif unix_delta <= DAY:
        return get_between_dates(con, gps, 0, date_from, date_to)
    elif unix_delta <= 3 * MONTH:
        return get_between_dates(con, gps, 1, date_from, date_to)
    else:
        return get_between_dates(con, gps, 2, date_from, date_to)


@app.post("/api/station/update")
async def update(req: Request, data: Data):
    token = get_token(req)
    format = "%d-%m-%Y %H:%M:%S"
    if token is None:
        return {"message": "no token found"}
    if not authorized_token(token):
        return {"message": "token is not valid"}
    update_weather(con, token["gps"], datetime.strftime(datetime.now(), format), data)
    return {"message": "weather updated successfulaly"}


@app.post("/api/station/register")
async def register(d: RegisterData):
    data = jsonable_encoder(d)
    if station_exists(con, data["gps"]):
        return {"message": "station already exists"}
    if not valid_input(con, data["gps"]):
        return {"message": "input data are not valid"}
    add_stations(con, data["gps"], data["serial_number"])
    return {"token": create_token(data["gps"], data["serial_number"])}
