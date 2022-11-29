from fastapi import FastAPI
from models import *

app = FastAPI()


# TODO: vrati GPS vsech stanic
@app.get("/api/all_stations")
async def all_stations():
    return {"message": ""}


# TODO: vrati aktualni pocasi ze stanice s danymi GPS 
@app.get("/api/now/{gps}")
async def now(gps: str):
    return {"message": ""}


# TODO: vrati vsechna namerena data ze stanice s danymi GPS
@app.get("/api/stats/{gps}")
async def stats(gps: str):
    return {"message": ""}


# TODO: (ZATIM NEDELAT) zaregistruje do databeze novou stanici s danymi GPS
@app.post("/api/register_station")
async def register_station():
    return {"message": ""}
