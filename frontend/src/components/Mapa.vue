<style scoped integrity="sha256-sA+zWATbFveLLNqWO2gtiw3HL/lh1giY/Inf1BJ0z14=" crossorigin="">
@import "https://unpkg.com/leaflet@1.9.2/dist/leaflet.css";
</style>

<script setup lang="ts">
//defineProps<{
//    msg: string
//}>()
import axios from "axios";
import L from 'leaflet'
import '../assets/leaflet-providers.js'
import { onBeforeUnmount, onDeactivated, onMounted } from "vue";
import type { StandardPropertiesFallback } from "csstype";

var icon = L.icon({
    iconUrl: 'src/assets/target.png',
    //shadowUrl: 'src/assets/map-pointer.png',

    iconSize: [20, 20], // size of the icon
    //shadowSize:   [50, 64], // size of the shadow
    iconAnchor: [10, 10], // point of the icon which will correspond to marker's location
    //shadowAnchor: [4, 62],  // the same for the shadow
    popupAnchor: [0, -15] // point from which the popup should open relative to the iconAnchor
});

// tady info: https://github.com/leaflet-extras/leaflet-providers
var map = L.map('map').setView([50.0835494, 14.4341414], 11); // Praha
L.tileLayer.provider('CartoDB.Voyager').addTo(map);



onBeforeUnmount(() => {
    map.off();
    map.remove();
});

onMounted(() => {
    axios
        .get("/api/stations")
        .then(response => {
            let stanice = response.data.station
            for (let i = 0; i < stanice.length; i++) {
                let souradnice = stanice[i].gps; //pak to vrátit debile
                let souradnice_split = stanice[i].gps.split("_");
                axios
                    .get("/api/now/" + souradnice)
                    .then(response => {
                        let stanice_obsah = response.data
                        if (stanice_obsah.message == "ok") {
                            console.log("fine")
                            L.marker([souradnice_split[0], souradnice_split[1]], {icon: icon}).addTo(map).bindPopup(`
                                <body>
                                    <h1>Stanice1</h1>
                                    <p>Můj milovaný bodík</p>
                                    <ul>
                                        <li>Teplota: ${stanice_obsah.temperature}</li>
                                        <li>Tlak: ${stanice_obsah.pressure}</li>
                                        <li>Rychlost vzduchu: ${stanice_obsah.temperature}</li>
                                        <li>Vlhkost: ${stanice_obsah.humidity}</li>
                                        <li>Rychlost větru: ${stanice_obsah.wind_speed}</li>
                                        <li>Směr větru: ${stanice_obsah.wind_direction}</li>
                                        <li>Srážky: ${stanice_obsah.rain}</li>
                                    </ul>
                                    <style>h1 {background-color: aqua;}</style>
                                </body>`, {offset: [115, 150]})

                        } else {
                            //jsme vpíči to vymyslí firu
                        }
                        // ulozim si to pocasi co mi prijde a potom to nasazim do toho BINDPOPUPu
                        //https://weathery.ecko.ga/, https://weathery.ecko.ga/docs#/default/now_api_now__gps__get
                    })
            }
        })
});

</script>


<template>
    <Obsah></Obsah>
</template>
