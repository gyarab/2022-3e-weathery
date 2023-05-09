<h2 align="center">Weathery</h2>
<p align="center"><b><a href="https://gyarab.github.io/2022-3e-weathery/main.pdf">Online PDF dokumentace</a></b></p>

<h4>Původní zadání</h4>
Aplikace bude mít tři části
- operace a vyrobení hardwaru, který bude měřit počasí (teplota, vlhkost, rychlost a směr větru, déšť) hardware bude obsluhovat Arduino, přičemž si čidla vyrobíme sami (rychlost a směr větru, měření deště)
- backend - sbírá data o počasí a ukládá je do databáze, backend bude fungovat i jako API pro jine vývojáře na zjištění aktuálního počasí
- frontend - webová aplikace zobrazující počasí (mapka, na které budou vidět všechny stanice a bude se dát zobrazit podrobnější data o dané stanici).

<h4>Instalace</h4>
<h6><a href="https://api.weathery.svs.gyarab.cz/">Backend</a></h6>

```sh
cd backend
docker build -t weathery .
docker run --network slirp4netns:allow_host_loopback=true -e DB_HOST={DB_HOST} -p {PORT}:5000  weathery
```

<h6><a href="https://weathery.svs.gyarab.cz/">Frontend</a></h6>


```sh
cd frontend
npm install
npm run dev
```

