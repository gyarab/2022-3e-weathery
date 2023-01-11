from pydantic import BaseModel


class RegisterData(BaseModel):
    gps: str  # (40.123455 -35.6543321)
    serial_number: int  # 123456


class Data(BaseModel):
    temperature: int  # C
    humidity: int  # %
    pressure: int  # Pa
    wind_speed: int  # km/h
    wind_direction: str  # directions
    rain: int  # mm/h
