# API docs

## GET "/api/stations"
vrati GPS vsech registrovanych stanic <br/> 
format dat:
```javascript
{
  "station": [
    {"gps": "str"},
    {"gps": "str"},
    ...
  ]
}
```

## GET "/api/now/{gps}"
vrati aktualni pocasi stanice s temito GPS <br/> 
format dat:
```javascript
{
  "time": "str"                // d-m-y H:M:S
  "temperature": "int",        // C
  "humidity": "int",           // %
  "pressure": "int",           // Pa
  "wind_speed": "int",         // km/h
  "wind_direction": "str",     // directions
  "rain": "int"                // mm/h 
}
```

## GET "/api/stats/{gps}?date_from={from}&date_to={to}"
vrati zprumerovane data v danem casomev intervalu <br/>
- (interval <= DEN) -> prumer z kazde hodiny 
- (interval <= 3 MESICE) -> prumer z kazdeho dne
- (interval > 3 MESICE) -> prumer z kazedeho tydne

```javascript
{
  "data": [
    {
      "time": "str",               // d-m-y H:M:S
      "temperature": "int",        // C
      "humidity": "int",           // %
      "pressure": "int",           // Pa
      "wind_speed": "int",         // km/h
      "wind_direction": "str",     // directions
      "rain": "int",               // mm/h
      "average_of": "int"          // sum  
    },
    {
      "time": "str",               // d-m-y H:M:S
      "temperature": "int",        // C
      "humidity": "int",           // %
      "pressure": "int",           // Pa
      "wind_speed": "int",         // km/h
      "wind_direction": "str",     // directions
      "rain": "int"                // mm/h 
      "average_of": "int"          // sum  
    },
    ...
  ]
}
```

## POST "/api/station/update"
server si pres token overi jaka stanice posila data a ulozi je do databaze pod prislusnou stanici

## POST "/api/station/register"
server si podle secret_key overi ze stanice je realna a vytvori ji token s kterym se pozdeji stanice prokazuje a dale stanici zapise do databaze
