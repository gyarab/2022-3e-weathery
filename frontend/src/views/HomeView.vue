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
        <div ref="druhyText" class="druhyText">
            <h2>Změny {{ rok_od }} - {{ rok_do }}</h2>
            <div class="hodnoty">
                <h1>Průměrná teplota:</h1>
                <h1>{{ procento('avg-temp') }}</h1>
                <h1>Průměrné srážky:</h1>
                <h1>{{ procento('avg-rain') }}</h1>
                <h1>Průměrná vlhkost:</h1>
                <h1>{{ procento('avg-hum') }}</h1>
                <h1>Průměrný tlak:</h1>
                <h1>{{ procento('avg-press') }}</h1>
            </div>
        </div>
        <div ref="scroll" id="scroll" @click="scrolluj({deltaY: 'tlacitko'})">
            <p>SCROLL</p>
            <img src="@/assets/icony/scroll.svg" alt="sipka dolu">
        </div>

    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "HomeView",
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

        if (window.innerWidth >= 1200) {
            document.body.style.height = "100vh"
            document.body.style.overflow = "hidden"
        } //zruší actual scrollování


        window.addEventListener("wheel", this.scrolluj)
    },
    unmounted() {
        window.removeEventListener('wheel', this.scrolluj);
        document.body.style.height = "100vh" //vrati actual scrollování
        document.body.style.overflow = "unset"
    },
    methods: {
        scrolluj(e) {
            if (window.innerWidth >= 1200) {
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
                this.$refs.b1.style.marginLeft = `-${this.scroll / 1.5}vh`

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
                this.$refs.b4.style.marginLeft = `${this.scroll}vh`

                this.$refs.prvniText.style.opacity = `${100 - (this.scroll / (max / 2) * 100)}%`
                this.$refs.druhyText.style.opacity = `${(this.scroll - max / 2) / (max / 2) * 100}%`

                if (this.scroll < 90) {
                    this.$refs.prvniText.style.display = 'block'
                    this.$refs.druhyText.style.display = 'none'
                    this.$refs.scroll.style.display = 'flex'
                } else if (this.scroll > 90) {
                    this.$refs.prvniText.style.display = 'none'
                    this.$refs.druhyText.style.display = 'block'
                    this.$refs.scroll.style.display = 'none'
                }

                this.$refs.scroll.style.opacity = `${100 - (this.scroll / (max / 3) * 100)}%`
            }
        },
        procento(udaj) {
            try {
                let a = this.data[udaj][this.rok_od]
                let b = this.data[udaj][this.rok_do]
                if (100 - (a / b) * 100 > 0) {
                    return `+${(100 - (a / b) * 100).toFixed(3)} %`
                }
                return `${(100 - (a / b) * 100).toFixed(3)} %`
            } catch (e) {
                return 'Načítání...'
            }
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
    display: none;
}

.hodnoty {
    display: grid;
    grid-template-columns: auto auto;
    justify-items: left;
    column-gap: 30px;
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

@media only screen and (max-width: 1200px) {
    #bloby {
        z-index: -10;
    }

    #blob1 {
        top: 10%;
        left: -30%;
        width: 100%;
    }

    #blob4 {
        top: 50%;
        left: 30%;
        width: 80%;
    }

    #blob3, #blob2 {
        display: none;
    }

    #scroll {
        display: none;
    }

    h1 {
        font-size: 1.5em !important;
    }

    .prvniText, .druhyText {
        width: 90% !important;
        display: block;
        opacity: 100%;
        color: black;
        position: absolute;
    }

    .prvniText {
        top: 25%;
        left: 5%;
        font-size: 5vw;
    }

    .druhyText {
        top: 58%;
        left: 5%;
        width: 80%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        gap: 10px;
        font-size: 3.5vw;

    }

    .druhyText h2 {
        font-weight: normal;
    }

    .home {
        display: block;
        z-index: 10;
    }

    body {
        overflow: visible !important;
    }
}
</style>