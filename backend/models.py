from pydantic import BaseModel


class LoginItem(BaseModel):
    name: str
    password: str


class RegisterData(BaseModel):
    gps: str  # (40.123455 -35.6543321)
    id: int  # 123456


class Data(BaseModel):
    temperature: float  # C
    humidity: float  # %
    pressure: float  # Pa
    wind_speed: float  # km/h
    wind_direction: str  # directions
    rain: float  # mm/h
