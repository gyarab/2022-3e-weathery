from random import randint
import env
import emails
from datetime import datetime, timedelta
import jwt
import json
import stripe
import hashlib
import secrets
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
    get_all_orders,
    user_exists,
    get_password,
    get_email,
    get_admin_emails,
    get_home_page_data,
)
from models import Data, RegisterData, LoginItem

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"

DAY = 86400
MONTH = 2678400

USER = env.DB_USER
PASSWORD = env.DB_PASSWORD
DB_NAME = env.DB_NAME
DB_HOST = env.DB_HOST
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

con = psycopg2.connect(
    database=DB_NAME, user=USER, password=PASSWORD, host=DB_HOST, port=5432
)


def get_salt():
    return secrets.token_hex(8)


def hash_password(plain_text_password):
    salt = get_salt()
    password = (plain_text_password + salt).encode("utf-8")
    hashed_password = hashlib.sha512(password).hexdigest()
    return f"{salt}${hashed_password}"


def verify_password(plain_text_password, hashed_password):
    salt = hashed_password.split("$")[0]
    password = (plain_text_password + salt).encode("utf-8")
    new_hash = hashlib.sha512(password).hexdigest()
    return f"{salt}${new_hash}" == hashed_password


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


def authorized(req: Request) -> bool:
    token = get_token(req)
    if token is None:
        return False
    if not user_exists(con, token["name"]):
        return False
    return True


def authorized_token(token) -> bool:
    if token is None:
        return False
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
def stats(gps: str, date_from: str = "day_ago", date_to: str = "now", freq: int = 0):
    if not station_exists(con, gps):
        return {"message": "station does not exist"}
    format = "%d-%m-%Y %H:%M:%S"
    if date_from == "day_ago":
        date_from = str(
            datetime.strftime(datetime.now() - timedelta(hours=24), "%d-%m-%Y %H:%M:%S")
        )
    if date_to == "now":
        date_to = str(datetime.strftime(datetime.now(), "%d-%m-%Y %H:%M:%S"))
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
        if unix_delta <= 3 * DAY:
            return get_between_dates(con, gps, 3, date_from, date_to)
        elif unix_delta <= 3 * MONTH:
            return get_between_dates(con, gps, 4, date_from, date_to)
        else:
            return get_between_dates(con, gps, 5, date_from, date_to)


@app.post("/station/update")
def station_update(req: Request, d: Data):
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
    return create_token(data["gps"], data["id"])


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

    if event["type"] == "charge.succeeded":
        data = event["data"]["object"]
        customer_data = {
            "id": int(str(randint(10000, 99999)) + str(event["created"])),
            "email": data["billing_details"]["email"],
            "name": data["billing_details"]["name"],
            "address": data["billing_details"]["address"],
            "date": datetime.fromtimestamp(event["created"]).strftime(
                "%d-%m-%Y %H:%M:%S"
            ),
            "stripe_json": json.dumps(event),
        }
        create_order(con, customer_data)
        emails.send_order_confirmation(
            customer_data["id"],
            customer_data["email"],
            customer_data["name"],
            customer_data["address"],
        )
        emails.send_new_order_notification(
            customer_data["id"],
            ", ".join(get_admin_emails(con)),
        )
    return 200


@app.get("/home")
def home():
    return get_home_page_data(con)


@app.get("/order/{id}")
def order(id: int):
    if not order_exists(con, id):
        return {"message": "order does not exist"}
    return get_order_details(con, id)


@app.get("/orders")
def orders(req: Request):
    if not authorized(req):
        return {"message": "you are not authorized"}
    return get_all_orders(con)


@app.post("/update/{id}")
def order_update(req: Request, id: int, state: int):
    if not authorized(req):
        return {"message": "you are not authorized"}
    if not order_exists(con, id):
        return {"message": "order does not exist"}
    if state == 1:
        update_order_state(con, id, "sent")
        emails.send_state_info(id, get_email(con, id), "odesláno")
    elif state == 0:
        update_order_state(con, id, "paid")
        emails.send_state_info(id, get_email(con, id), "zaplaceno")
    else:
        return {"message": "invalid state"}

    return {"message": "order state updated"}


@app.post("/login")
def login(login_item: LoginItem):
    login_data = jsonable_encoder(login_item)
    if not user_exists(con, login_data["name"]):
        return {"message": "login failed"}
    if not verify_password(
        login_data["password"], get_password(con, login_data["name"])
    ):
        return {"message": "wrong password"}
    payload = {
        "name": login_data["name"],
    }
    return {"token": jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)}
