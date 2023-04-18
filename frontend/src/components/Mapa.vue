<style scoped integrity="sha256-sA+zWATbFveLLNqWO2gtiw3HL/lh1giY/Inf1BJ0z14=" crossorigin="">
@import "https://unpkg.com/leaflet@1.9.2/dist/leaflet.css";
</style>

<script lang="ts">
import axios from "axios";
import L from 'leaflet'
import '../assets/leaflet-providers'

export default {
    name: 'Mapa',
    data() {
        return {
            icon: L.icon({
                iconUrl: 'src/assets/icony/target.png',
                iconSize: [30, 30], // size of the icon
                iconAnchor: [20, 35], // point of the icon which will correspond to marker's location
                popupAnchor: [-5, -7] // point from which the popup should open relative to the iconAnchor
            }),
            map: L.map('map').setView([50.0835494, 14.4341414], 11), // Praha
        }
    },
    mounted() {
        // tady info: https://github.com/leaflet-extras/leaflet-providers
        L.tileLayer.provider('CartoDB.Voyager').addTo(this.map);

        axios
            .get("/stations")
            .then(response => {
                let stanice = response.data.station
                for (let i = 0; i < stanice.length; i++) {
                    let souradnice = stanice[i].gps; //pak to vrátit debile
                    let souradnice_split = stanice[i].gps.split("_");
                    axios
                        .get("/now/" + souradnice)
                        .then(response => {
                            let stanice_obsah = response.data
                            if (stanice_obsah.message == "ok") {
                                let marker = L.marker([souradnice_split[0], souradnice_split[1]], {icon: this.icon}).addTo(this.map);
                                marker.bindPopup(`
                                    <body>
                                        <h1 class="nadpis-popup" >${souradnice.replace("_", "° N ").replaceAll(".", ",")}° E</h1> <!-- seru na to more mozna nekdy z toho udelame router-link -->
                                        <hr>
                                        <div id="container">
                                            <img class="icony_popup zmensitMin" src="src/assets/icony/teplota.svg" alt="teplota"><h2>${stanice_obsah.temperature}°C</h2>
                                            <img class="icony_popup zmensitVic" src="src/assets/icony/tlak.svg" alt="tlak"><h2>${Math.round(stanice_obsah.pressure / 10) / 10} hPa</h2>
                                            <img class="icony_popup zmensitVic" src="src/assets/icony/vlhkost.svg" alt="vlhkost"><h2>${stanice_obsah.humidity}%</h2>
                                            <img class="icony_popup zmensitMin" src="src/assets/icony/vitr.svg" alt="vitr"><h2>${stanice_obsah.wind_speed}m/s</h2>
                                            <img class="icony_popup zmensit" src="src/assets/icony/smer.svg" alt="smer"><h2>${stanice_obsah.wind_direction}</h2>
                                            <img class="icony_popup zmensit" src="src/assets/icony/dest.svg" alt="dest"><h2>${stanice_obsah.rain} mm/h</h2>
                                        </div>
                                        <span id="flex"><a href="${souradnice.replace('_', '-').replaceAll('.', ',')}" id="popup-btn">Zobrazit více</a></span>
                                        <style>
                                            #popup-btn {
                                                text-decoration: none;
                                                text-align: center;
                                                font-size: 1.2em;
                                            }
                                            #flex {
                                                margin-top: 20px;
                                                margin-bottom: 10px;
                                                display: flex;
                                                align-items: center;
                                                justify-content: center;
                                            }
                                            .nadpis-popup {
                                                text-decoration: none;
                                                font-weight: bold;
                                                color: #333 !important;
                                                font-size: 2em;
                                            }
                                            img {
                                                user-select: none;
                                            }
                                            #container {
                                                display: grid;
                                                grid-template-columns: 40px auto;
                                                column-gap: 10px;
                                            }
                                        </style>
                                    </body>`, {offset: [180, 201], maxWidth: 250})
                            } else {
                                //jsme vpíči to vymyslí firu
                            }
                        })
                }
            })
    },
    beforeUnmount() {
        this.map.off();
        this.map.remove();
    },
}
</script>

<template>
    <Obsah></Obsah>
</template>
