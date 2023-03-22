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
                iconUrl: 'src/assets/icony/target2.png',
                iconSize: [40, 40], // size of the icon
                iconAnchor: [20, 35], // point of the icon which will correspond to marker's location
                popupAnchor: [8, -32] // point from which the popup should open relative to the iconAnchor
            }),
            map: L.map('map').setView([50.0835494, 14.4341414], 11), // Praha

        }
    },
    mounted() {
        // tady info: https://github.com/leaflet-extras/leaflet-providers
        L.tileLayer.provider('CartoDB.Positron').addTo(this.map);

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
                                        <a href="${souradnice.replace('_', '-').replaceAll('.', ',')}" class="nadpis-popup" ><h1>${souradnice.replace("_", "° S ").replaceAll(".", ",")}° E</h1></a> <!-- seru na to more mozna nekdy z toho udelame router-link -->
                                        <hr>
                                        <h2><img class="icony_popup" src="src/assets/icony/teplo.svg" alt="Teplota">${stanice_obsah.temperature}°C</h2>
                                        <h2><img class="icony_popup" src="src/assets/icony/tlak.png" alt="Teplota">${Math.round(stanice_obsah.pressure / 10) / 10} hPa</h2>
                                        <h2><img class="icony_popup" src="src/assets/icony/vlhkost.svg" alt="Teplota">${stanice_obsah.humidity}%</h2>
                                        <h2><img class="icony_popup" src="src/assets/icony/vitr.svg" alt="Teplota">${stanice_obsah.wind_speed}m/s</h2>
                                        <h2><img class="icony_popup" src="src/assets/icony/smer_vetru.png" alt="Teplota">${stanice_obsah.wind_direction}</h2>
                                        <h2><img class="icony_popup" src="src/assets/icony/dest.svg" alt="Teplota">${stanice_obsah.rain} mm/h</h2>
                                        <style>
                                            .nadpis-popup {
                                                text-decoration: none;
                                                color: #333 !important;
                                            }
                                            h1 {
                                                font-weight: bold;
                                                font-size: 2em;
                                            }
                                            .default-time-selector {
                                                height: 25px;
                                            }
                                            .nadpis-second-popup {
                                                font-size: 22px;
                                                text-align: center;
                                                text-decoration: none;
                                            }
                                        </style>
                                    </body>`, {offset: [180, 201], maxWidth: 250})
                            } else {
                                //jsme vpíči to vymyslí firu
                            }
                            // ulozim si to pocasi co mi prijde a potom to nasazim do toho bindPOPUPu
                            //https://weathery.ecko.ga/, https://weathery.ecko.ga/docs#/default/now_api_now__gps__get
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
