# API docs

## GET"/api/stations"
vrati GPS vsech registrovanych stanic \ 
format dat:
```
{
  "stations": [
    {"gps": str}
    {"gps": str}
    ...
  ]
}
```

## GET"/api/now/{gps}"
vrati aktualni pocasi stanice s temito GPS \
format dat:
```
{
  "temperature": int        # C
  "humidity": int           # %
  "preasure": int           # Pa
  "wind_speed": int         # km/h
  "wind_direction": str     # directions
  "rain": int               # mm/h 
}
```

## GET"/api/stats/{gps}"
vrati schena namerena data z dane stanice

## POST"/api/update"
server si pres token overi jaka stanice posila data a ulozi je do databaze pod prislusnou stanici

## POST"/api/register"
server si podle secret_key overi ze stanice je realna a vytvori ji token s kterym se pozdeji stanice prokazuje a dale stanici zapise do databaze
