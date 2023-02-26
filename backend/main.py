from random import randint
import env
import emails
from datetime import datetime
import jwt
import stripe
import psycopg2
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
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
    id_exists,
    update_station,
    create_order,
    update_order_state,
    order_exists,
    get_order_details,
)
from models import Data, RegisterData

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"

DAY = 86400
MONTH = 2678400

USER = env.DB_USER
PASSWORD = env.DB_PASSWORD
DB_NAME = env.DB_NAME
STRIPE_SEC = env.STRIPE_SEC
WEBHOOK_SEC = env.WEBHOOK_SEC


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stripe.api_key = STRIPE_SEC
"""
con = psycopg2.connect(
    database=DB_NAME, user=USER, password=PASSWORD, host="localhost", port=5432
)


def get_token(req):
    try:
        token = req.headers["Authorization"].split()[1]
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[
                ALGORITHM,
            ],
        )
    except:
        return None


def authorized_token(token) -> bool:
    return station_exists(con, token["gps"])


def create_token(gps, id):
    payload = {"gps": gps, "id": id}
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.get("/stations")
def stations():
    return get_all_stations(con)


@app.get("/now/{gps}")
def now(gps: str):
    if not station_exists(con, gps):
        return {"message": "station does not exist"}
    return get_latest_data(con, gps)


@app.get("/stats/{gps}")
def stats(gps: str, date_from: str, date_to: str = "now", freq: int = 0):
    if not station_exists(con, gps):
        return {"message": "station does not exist"}
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
    if freq > 0 and freq < 8:
        return get_between_dates(con, gps, freq, date_from, date_to)
    else:
        if unix_delta <= DAY:
            return get_between_dates(con, gps, 3, date_from, date_to)
        elif unix_delta <= 3 * MONTH:
            return get_between_dates(con, gps, 4, date_from, date_to)
        else:
            return get_between_dates(con, gps, 5, date_from, date_to)


@app.post("/station/update")
def update(req: Request, d: Data):
    token = get_token(req)
    data = jsonable_encoder(d)
    format = "%d-%m-%Y %H:%M:%S"
    if token is None:
        return {"message": "no token found"}
    if not authorized_token(token):
        return {"message": "token is not valid"}
    update_weather(con, token["id"], datetime.strftime(datetime.now(), format), data)
    return {"message": "weather updated successfulaly"}


@app.post("/station/register")
def register(d: RegisterData):
    data = jsonable_encoder(d)
    if not valid_input(con, data["id"]):
        return ""
    if not id_exists(con, data["id"]):
        add_stations(con, data["gps"], data["id"])
        return create_token(data["gps"], data["id"])
    update_station(con, data["id"], data["gps"])
    return create_token(data["gps"], data["id"])"""


@app.post("/payment-webhook")
async def webhook(req: Request):
    payload = await req.body()
    sig_header = req.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(
            payload,
            str(sig_header),
            WEBHOOK_SEC,
        )
    except ValueError:
        return 400

    if event["type"] == "payment_intent.succeeded":
        data = event["data"]["object"]
        customer_data = {
            "id": int(str(randint(10000, 99999)) + data["created"]),
            "email": data["receipt_email"],
            "name": data["shipping"]["name"],
            "phone": data["shipping"]["phone"],
            "address": data["shipping"]["address"],
            "date": datetime.fromtimestamp(data["created"]).strftime(
                "%d-%m-%Y %H:%M:%S"
            ),
            "stripe_json": event,
        }
        # create_order(con, customer_data)
        emails.send_order_confirmation(
            customer_data["id"],
            customer_data["email"],
            customer_data["name"],
            customer_data["phone"],
            customer_data["address"],
        )
    return 200


@app.get("/order/{id}")
def order(id: int):
    if not order_exists(con, id):
        return {"message": "order does not exist"}
    return get_order_details(con, id)
