<style scoped integrity="sha256-sA+zWATbFveLLNqWO2gtiw3HL/lh1giY/Inf1BJ0z14=" crossorigin="">
@import "https://unpkg.com/leaflet@1.9.2/dist/leaflet.css";
</style>

<script setup lang="ts">
//defineProps<{
//    msg: string
//}>()
import L from 'leaflet'
import '../assets/leaflet-providers.js'

// tady info: https://github.com/leaflet-extras/leaflet-providers
var map = L.map('map').setView([50.0835494, 14.4341414], 11); //praha 50.0835494N, 14.4341414E
/*L.tileLayer.provider('Jawg.Light', {
    accessToken: 'nWDyoQqkjWUxatUXlNdKTqJymEWIFq0glO5O4kk5Ir3pUsmGb45lqJaHRyLz1OSo'
}).addTo(map);*/
L.tileLayer.provider('CartoDB.Voyager').addTo(map);

</script>


<template>
</template>

