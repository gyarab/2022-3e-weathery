import psycopg2
import env
from manage_data import update_weather

USER = env.DB_USER
PASSWORD = env.DB_PASSWORD
DB_NAME = env.DB_NAME

con = psycopg2.connect(
    database=DB_NAME, user=USER, password=PASSWORD, host="localhost", port=5432
)


def post_data(con):
    date = "16-12-2022"
    gps = "50.1337883 14.3781242"
    for i in range(24):
        for j in range(12):
            data = {
                "temperature": i,
                "humidity": i * 5,
                "pressure": i * 1000,
                "wind_speed": i * 2,
                "wind_direction": "N",
                "rain": i,
            }
            update_weather(
                con,
                gps,
                f"{date} {i}:{j*5}:42",
                data,
            )


post_data(con)
