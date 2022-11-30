# API docs

## GET"/api/stations"
vrati GPS vsech registrovanych stanic

## GET"/api/now/{gps}"
vrati aktualni pocasi stanice s temito GPS 

## GET"/api/stats/{gps}"
vrati schena namerena data z dane stanice

## POST"/api/update"
server si pres token overi jaka stanice posila data a ulozi je do databaze pod prislusnou stanici

## POST"/api/register"
server si podle secret_key overi ze stanice je realna a vytvori ji token s kterym se pozdeji stanice prokazuje a dale stanici zapise do databaze
