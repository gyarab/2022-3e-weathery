<template>
    <div id="bloby">
        <img ref="b1" src="@/assets/blob1.svg" id="blob1" alt="blob">
        <img ref="b2" src="@/assets/blob2.svg" id="blob2" alt="blob">
        <img ref="b3" src="@/assets/blob3.svg" id="blob3" alt="blob">
        <img ref="b4" src="@/assets/blob4.svg" id="blob4" alt="blob">
    </div>
    <div class="home">
        <div ref="prvniText" class="prvniText">
            <h1>Dlouhodobá data sledující změnu klimatu</h1>
        </div>
        <div ref="druhyText" class="druhyText" v-if="data['avg-temp']">
            <h2>Změny {{ rok_od }} - {{ rok_do }}</h2>
            <div class="hodnoty">
                <h1>Průměrná teplota:</h1><h1>{{ procento('avg-temp')}}</h1>
                <h1>Průměrné srážky:</h1><h1>{{ procento('avg-rain') }}</h1>
                <h1>jeste dalsi dam neboj</h1><h1>Sus</h1>
            </div>
        </div>
        <div ref="scroll" id="scroll" @click="scrolluj({deltaY: 'tlacitko'})">
            <p>SCROLL</p>
            <img src="src/assets/icony/scroll.svg" alt="sipka dolu">
        </div>

    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "HomeView.vue",
    data() {
        return {
            scroll: 0,
            data: {},
            rok_od: '?', // to se ukaze pokud se neco posere
            rok_do: '?'
        }
    },
    mounted() {
        axios.get("/home", {}).then(response => {
            this.data = response.data
            this.rok_od = Object.keys(this.data['avg-rain'])[0]
            this.rok_do = Object.keys(this.data['avg-rain'])[1]
        })

        document.body.style.height = "100vh" //zruší actual scrollování
        document.body.style.overflow = "hidden"

        window.addEventListener("wheel", this.scrolluj)
    },
    unmounted() {
        window.removeEventListener('wheel', this.scrolluj);
    },
    methods: {
        scrolluj(e) {
            let rychlost = 15
            let min = 0
            let max = 180
            if (e.deltaY === 'tlacitko') {
                this.scroll = max
            } else if (e.deltaY > 0) {
                this.scroll += rychlost
            } else {
                this.scroll -= rychlost
            }
            if (this.scroll < min) { // spodni hranice
                this.scroll = min
            } else if (this.scroll > max) { // horni hranice
                this.scroll = max
            }

            // nesahat pls 362,4h práce
            this.$refs.b1.style.transform = `rotate(${this.scroll / max * 180}deg)`
            this.$refs.b1.style.width = `${32 + this.scroll}%`
            this.$refs.b1.style.marginTop = `-${this.scroll / 3.9}vh`
            this.$refs.b1.style.marginLeft = `-${this.scroll / 2}vh`

            this.$refs.b2.style.transform = `rotate(${this.scroll / max * 120}deg)`
            this.$refs.b2.style.width = `${40 - this.scroll / 10}%`
            this.$refs.b2.style.marginTop = `${this.scroll}vh`
            this.$refs.b2.style.marginLeft = `-${this.scroll / 2}vh`

            this.$refs.b3.style.transform = `rotate(${-this.scroll / max * 60}deg)`
            this.$refs.b3.style.width = `${30 - this.scroll / 10}%`
            this.$refs.b3.style.marginTop = `${this.scroll / 2}vh`
            this.$refs.b3.style.marginLeft = `${this.scroll / 2}vh`

            this.$refs.b4.style.transform = `rotate(${this.scroll / max * 120}deg)`
            this.$refs.b4.style.width = `${25 - this.scroll / 10}%`
            this.$refs.b4.style.marginLeft = `${this.scroll / 1.2}vh`

            this.$refs.prvniText.style.opacity = `${100 - (this.scroll / (max/2) * 100)}%`
            this.$refs.druhyText.style.opacity = `${(this.scroll - max / 2)  / (max / 2) * 100}%`

            this.$refs.scroll.style.opacity = `${100 - (this.scroll / (max / 3) * 100)}%`
        },
        procento(udaj) {
            let a = this.data[udaj][this.rok_od]
            let b = this.data[udaj][this.rok_do]
            if (100 - (a / b) * 100 > 0) {
                return `+${(100 - (a / b) * 100).toFixed(3)} %`
            }
            return `${ (100 - (a / b) * 100).toFixed(3) } %`
        }
    }
}
</script>

<style scoped>
.home {
    display: grid;
    align-items: center;
    justify-items: center;
    width: 100vw;
    height: 100vh;
    position: absolute;
    z-index: 10;
}

#scroll {
    position: absolute;
    bottom: 10%;
    font-family: Inter, sans-serif;
    font-size: 14px;
    display: flex;
    flex-wrap: wrap;
    width: 10px;
    justify-content: center;
    cursor: pointer;
    user-select: none;
    transition-duration: 0.5s;
}

#scroll img {
    height: 20px;
}

.prvniText {
    width: 45%;
    text-align: center;
    transition-duration: 0.5s;
    position: absolute;
}

.druhyText {
    opacity: 0;
    position: absolute;
    text-align: center;
    transition-duration: 0.5s;
    color: white;
}

.hodnoty {
    display: grid;
    grid-template-columns: auto auto;
    justify-items: left;
    column-gap: 10px;
}

#bloby {
    position: absolute;
    width: 100vw;
    height: 100vh;
    user-select: none;
}

#bloby img {
    transition-duration: 0.5s; /*aby to bylo smooth*/
    position: absolute;
}

#blob1 {
    top: 10%;
    left: 10%;
    width: 32%;
    z-index: -10;
}

#blob2 {
    top: 52%;
    left: 12%;
    width: 40%;
}

#blob3 {
    top: 40%;
    left: 55%;
    width: 30%;
}

#blob4 {
    top: 5%;
    left: 48%;
    width: 25%;
}
</style>