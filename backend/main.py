from fastapi import FastAPI, Request
from models import Data

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


# TODO: z tokenu zjisti gps souradnice a prida do databaze aktualni prijate hodnoty ze stanice
@app.post("/api/update")
async def update(req: Request, data: Data):
    return {"message": ""}


# TODO: (ZATIM NEDELAT) vytvori token pro danou stanici a zaregistruje ji do databeze
@app.post("/api/register_station")
async def register_station():
    return {"message": ""}
