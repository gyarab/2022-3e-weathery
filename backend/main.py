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

WEEK = 604800

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


# TODO: vrati GPS vsech stanic
@app.get("/api/stations")
async def stations():
    return get_all_stations(con)


# TODO: vrati aktualni pocasi ze stanice s danymi GPS
@app.get("/api/now/{gps}")
async def now(gps: str):
    if not station_exists(con, gps):
        return {"message": "staion does not exist"}
    return get_latest_data(con, gps)


# TODO: vrati vsechna namerena data ze stanice s danymi GPS
@app.get("/api/stats/{gps}/{date_from}/{date_to}")
async def stats(gps: str, date_from: str, date_to: str):
    format = "%d-%m-%Y %H:%M:%S"
    if not valid_date(date_from):
        return {"message": "date is not valid"}
    if not valid_date(date_to):
        return {"message": "date is not valid"}
    if len(date_from) <= 10:
        date_from += " 00:00:00"
    if len(date_to) <= 10:
        date_to += " 23:59:59"
    delta = datetime.strptime(date_to, format) - datetime.strptime(date_from, format)
    unix_delta = datetime.timestamp(
        datetime.strptime(date_to, format)
    ) - datetime.timestamp(datetime.strptime(date_from, format))
    if unix_delta <= 0:
        return {"message": "date is not valid"}
    return get_between_dates(con, gps, date_from, date_to)


# TODO: z tokenu zjisti gps souradnice a prida do databaze aktualni prijate hodnoty ze stanice
@app.post("/api/staion/update")
async def update(req: Request, data: Data):
    token = get_token(req)
    format = "%d-%m-%Y %H:%M:%S"
    if token is None:
        return {"message": "no token found"}
    if not authorized_token(token):
        return {"message": "token is not valid"}
    update_weather(con, token["gps"], datetime.strftime(datetime.now(), format), data)
    return {"message": "weather updated successfulaly"}


# TODO: (ZATIM NEDELAT) overi si podle serial_number (seriove cislo stanice), ze stanice je realna
# a vytvori pro ni token, ktery ji posle a zaregistruje ji do databeze
@app.post("/api/staion/register")
async def register(d: RegisterData):
    data = jsonable_encoder(d)
    if station_exists(con, data["gps"]):
        return {"message": "staion already exists"}
    if not valid_input(con, data["gps"]):
        return {"message": "input data are not valid"}
    add_stations(con, data["gps"], data["serial_number"])
    return {"token": create_token(data["gps"], data["serial_number"])}
