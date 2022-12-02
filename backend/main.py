import env
from time import time
import jwt
import psycopg2
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from manage_data import add_stations, get_all_stations, station_exists, update_weather, valid_input
from models import Data, RegisterData

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"

WEEK = 604800

USER = env.USER
PASSWORD = env.PASSWORD

app = FastAPI()
con = psycopg2.connect(database="weatherydb", user=USER,
                       password=PASSWORD, host="localhost", port=5432)


def get_token(req):
    try:
        token = req.headers["Authorization"].split()[1]
        return jwt.decode(token, SECRET_KEY)
    except KeyError:
        return None


def authorized_token(token) -> bool:
    return station_exists(con, token["gps"], token["serial_number"])


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
    return {"message": ""}


# TODO: vrati vsechna namerena data ze stanice s danymi GPS
@app.get("/api/stats/{gps}")
async def stats(gps: str, date_from: int = int(time()-WEEK), data_to: int = int(time())):
    return {"message": ""}


# TODO: z tokenu zjisti gps souradnice a prida do databaze aktualni prijate hodnoty ze stanice
@app.post("/api/update")
async def update(req: Request, data: Data):
    token = get_token(req)
    if token is None:
        return {"message": "no token found"}
    if not authorized_token(token):
        return {"message": "token is not valid"}
    update_weather(con, token["gps"],
                   token["serial_number"], int(time()), data)
    return {"message": "weather updated successfulaly"}


# TODO: (ZATIM NEDELAT) overi si podle serial_number (seriove cislo stanice), ze stanice je realna
# a vytvori pro ni token, ktery ji posle a zaregistruje ji do databeze
@app.post("/api/register")
async def register(d: RegisterData):
    data = jsonable_encoder(d)
    if station_exists(con, data["gps"], data["serial_number"]):
        return {"message": "staion already exists"}
    if not valid_input(con, data["gps"], data["serial_number"]):
        return {"message": "input data are not valid"}
    add_stations(con, data["gps"], data["serial_number"])
    return {"token": create_token(data["gps"], data["serial_number"])}
