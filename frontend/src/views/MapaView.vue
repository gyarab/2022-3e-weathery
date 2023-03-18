<script lang="ts">
//import TheWelcome from '../components/TheWelcome.vue'
import Mapa from '../components/Mapa.vue'

export default {
    components: {
        Mapa
    }
}
</script>

<template>
    <div id="map"></div>
    <Mapa/>
</template>

<style scoped>
#map {
    height: calc(100vh - var(--vyska-menu) - 1px);
}
</style>
