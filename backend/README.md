# API docs

## GET "/api/stations"
vrati GPS vsech registrovanych stanic <br/> 
format dat:
```json
{
  "stations": [
    {"gps": "str"}
    {"gps": "str"}
    ...
  ]
}
```

## GET "/api/now/{gps}"
vrati aktualni pocasi stanice s temito GPS <br/> 
format dat:
```json
{
  "temperature": "int"        // C
  "humidity": "int"           // %
  "pressure": "int"           // Pa
  "wind_speed": "int"         // km/h
  "wind_direction": "str"     // directions
  "rain": "int"               // mm/h 
}
```

## GET "/api/stats/{gps}/{from}/{to}"
vrati data v danem casomev intervalu <br/>
```json
{
  "data": [
    {
      "time": "str",
      "temperature": "int"        // C
      "humidity": "int"           // %
      "pressure": "int"           // Pa
      "wind_speed": "int"         // km/h
      "wind_direction": "str"     // directions
      "rain": "int"               // mm/h 
    },
    {
      "time": "str",
      "temperature": "int"        // C
      "humidity": "int"           // %
      "pressure": "int"           // Pa
      "wind_speed": "int"         // km/h
      "wind_direction": "str"     // directions
      "rain": "int"               // mm/h 
    },
    ...
  ]
}
```

## POST "/api/station/update"
server si pres token overi jaka stanice posila data a ulozi je do databaze pod prislusnou stanici

## POST "/api/station/register"
server si podle secret_key overi ze stanice je realna a vytvori ji token s kterym se pozdeji stanice prokazuje a dale stanici zapise do databaze
