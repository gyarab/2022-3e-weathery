<template>
    <header>
        <nav id="menu">
            <RouterLink to="/">Domů</RouterLink>
            <RouterLink to="/mapa">Mapa</RouterLink>
            <RouterLink to="/about">O nás</RouterLink>
            <h1>WEATHERY</h1>
            <RouterLink id="kosik" to="/nakup"><img src="@/assets/icony/kosik.svg" alt="kosik"></RouterLink>
            <img id="hamburger" src="@/assets/icony/hamburger.svg" alt="hamburger" @click="switchMenu">

        </nav>

        <div id="rollin" v-if="rollMenu" ref="rollin">
            <RouterLink to="/">Domů</RouterLink>
            <RouterLink to="/mapa">Mapa</RouterLink>
            <RouterLink to="/about">O nás</RouterLink>
            <RouterLink id="kosik" to="/nakup"><img src="@/assets/icony/kosik.svg" alt="kosik"></RouterLink>
        </div>

    </header>

    <RouterView/>

</template>

<script>
import {RouterLink, RouterView} from 'vue-router'

export default {
    name: 'App',
    data() {
        return {
            rollMenu: false
        }
    },
    methods: {
        switchMenu() {
            this.rollMenu = !this.rollMenu
        }
    }
}
</script>

<style scoped>
#hamburger {
    display: none;
}

#kosik {
    margin-left: auto;
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
    user-select: none;
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
    transition-duration: 0.2s;
}

#menu a:hover {
    font-size: 1.31em;
    padding: 0 11px;
    transition-duration: 0.2s;
}

@media only screen and (max-width: 1200px) {
    #menu a {
        display: none;
    }

    #menu {
        justify-content: right;
    }

    #hamburger {
        display: block;
        width: 30px;
        z-index: 10;
    }

    #menu h1 {
        top: 3px;
    }

    #rollin {
        display: flex;
        flex-direction: column;
        justify-content: left;
        position: absolute;
        background-color: var(--bila);
        width: 100%;
        z-index: 100;
    }

    #rollin a {
        font-family: Inter, sans-serif;
        font-size: var(--velikost-pisma-menu);
        color: black;
        text-align: center;
        text-decoration: none;
        vertical-align: middle;
        line-height: var(--vyska-menu);
        padding: 0 10px;
        z-index: 10;
        transition-duration: 0.2s;
    }

    #kosik {
        margin: 0;
    }
}
</style>