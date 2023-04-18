<script setup lang="ts">
import {RouterLink, RouterView} from 'vue-router'
</script>

<template>
    <header>
        <nav id="menu">
            <RouterLink to="/">Domů</RouterLink>
            <RouterLink to="/mapa">Mapa</RouterLink>
            <RouterLink to="/about">O nás</RouterLink>
            <h1>WEATHERY</h1>
            <RouterLink id="kosik" to="/nakup"><img src="src/assets/icony/kosik.svg" alt="kosik"></RouterLink>
        </nav>

    </header>

    <RouterView/>

</template>

<style scoped>
#kosik {
    margin-left: auto;
    user-select: none;
}

#kosik img {
    padding-top: 18px;
}

h1 {
    font-size: 35px;
    text-align: center;
    line-height: var(--vyska-menu);
    width: 300px;
    position: absolute;
    right: calc(50% - 150px);
    z-index: 10;
    letter-spacing: 2px;
    font-family: 'STIX Two Text', serif;
    mix-blend-mode: difference;
    color: var(--modra);
    /*#095e30*/
}

#menu {
    height: var(--vyska-menu);
    padding: 0 15px;
    display: flex;
}

#menu a {
    font-family: Inter, sans-serif;
    font-size: var(--velikost-pisma-menu);
    color: black;
    text-align: center;
    text-decoration: none;
    vertical-align: middle;
    line-height: var(--vyska-menu);
    padding: 0 15px;
    z-index: 10;
}
</style>