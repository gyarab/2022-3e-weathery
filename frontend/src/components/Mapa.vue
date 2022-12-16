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
import {onBeforeUnmount, onDeactivated, onMounted} from "vue";

var icon = L.icon({
    iconUrl: 'src/assets/target.png',
    //shadowUrl: 'src/assets/map-pointer.png',

    iconSize:     [20, 20], // size of the icon
    //shadowSize:   [50, 64], // size of the shadow
    iconAnchor:   [10, 10], // point of the icon which will correspond to marker's location
    //shadowAnchor: [4, 62],  // the same for the shadow
    popupAnchor:  [0, -15] // point from which the popup should open relative to the iconAnchor
});

// tady info: https://github.com/leaflet-extras/leaflet-providers
var map = L.map('map').setView([50.0835494, 14.4341414], 11); // Praha
L.tileLayer.provider('CartoDB.Voyager').addTo(map);

L.marker([50.13378832240194, 14.378124229373308], {icon: icon}).addTo(map)
    .bindPopup('Subemelaradio <br> muj house neraidovat pls')
var hruskq = L.marker([50.0742633, 14.3588950], {icon: icon}).addTo(map).bindPopup('plná taška hulení')
hruskq.bindPopup
        ("<h1>Stanice1</h1><p>Můj milovaný bodík</p><ul><li>Teplota:{{stanice1.teplota}}</li><li>Tlak: {{stanice1.tlak}}</li><li>Rychlost vzduchu: {{stanice1.rychlost_vzduchu}}</li></ul>")
    


onBeforeUnmount(() => {
   map.off();
   map.remove();
});

onMounted(() => {
    axios
        .get("/api/stations")
        .then(response => {
            // neco s tim co ti prijde more
        })
});

</script>


<template>
</template>
