from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from models import Data, RegisterData
import jwt
import psycopg2
import env

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"

USER = env.USER
PASSWORD = env.PASSWORD

app = FastAPI()


def get_connection():
    return psycopg2.connect(database="postgres", user=USER, password=PASSWORD, host="localhost", port=5432)


conn = get_connection()


def get_token(req):
    try:
        token = req.headers["Authorization"].split()[1]
        return token
    except KeyError:
        return None


def authorize_token(token):
    data = jwt.decode(token, SECRET_KEY)
    # if stations_exists(data['gps']):
    #    return True
    # return False


def create_token(gps, secret_key):
    payload = {'gps': gps, "secret_key": secret_key}
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# TODO: vrati GPS vsech stanic
@app.get("/api/stations")
async def stations(t):
    data = jwt.decode(t, SECRET_KEY, algorithms=[ALGORITHM])
    return {"message": data["gps"]}


# TODO: vrati aktualni pocasi ze stanice s danymi GPS 
@app.get("/api/now/{gps}")
async def now(gps: str):
    return {"message": ""}


# TODO: vrati vsechna namerena data ze stanice s danymi GPS
@app.get("/api/stats/{gps}")
async def stats(gps: str):
    return {"message": ""}


# TODO: z tokenu zjisti gps souradnice a prida do databaze aktualni prijate hodnoty ze stanice
@app.post("/api/update")
async def update(req: Request, data: Data):
    return {"message": ""}


# TODO: (ZATIM NEDELAT) overi si podle secret_key (seriove cislo stanice), ze stanice je realna
# a vytvori pro ni token, ktery ji posle a zaregistruje ji do databeze
@app.post("/api/register")
async def register(d: RegisterData):
    data = jsonable_encoder(d)
    return {"token": create_token(data["gps"], data["secret_key"])}
