from pydantic import BaseModel

class Data(BaseModel):
    temperature: int        # C
    humidity: int           # %
    preasure: int           # Pa
    wind_speed: int         # km/h
    wind_direction: int     # directions
    rain: int               # mm/h
