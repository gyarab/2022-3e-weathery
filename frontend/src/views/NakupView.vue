<template>
    <div class="nakup">
        <h1>Weathery stanice v1</h1>

        <div id="container">
            <div id="fotky">
                <img v-if="cisloFotky[0] === 1" class="obrazek" src="@/assets/stanice0.jpg" alt="Fotka stanice 1">
                <img v-else-if="cisloFotky[0] === 2" class="obrazek" src="@/assets/stanice1.jpg" alt="Fotka stanice 2">

                <img class="sipka" id="sipka1" src="@/assets/icony/sipka.svg" alt="Šipka" style="transform: scaleX(-1);" @click="fotoMinus">
                <img class="sipka" id="sipka2" src="@/assets/icony/sipka.svg" alt="Šipka" @click="fotoPlus">
            </div>

            <div id="text">
                <h2>Domácí meterologická stanice se schopnostmi profesionálního stroje?</h2>
                <p>
                    To je naše Weathery stanice která dokáže měřit aktuální teplotu, srážky, rychlost a směr větru, tlak a vlhkost vzduchu.
                    Všechna tyto data poté posílá na náš server kde se po registraci budou na příslušných souřadniciích zobrazovat naměřená data.
                </p>
                <div id="koupit">
                    <h2 style="vertical-align: middle;">2 499,99 Kč</h2>
                    <button class="btn" onclick="window.location.href = 'https://buy.stripe.com/test_aEU4hqeOt0Freje288'">Koupit</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "NakupView",
    data() {
        return {
            cisloFotky: [1,2]
        }
    },
    methods: {
        fotoPlus() {
            if (this.cisloFotky[0] === this.cisloFotky[1]) {
                this.cisloFotky[0] = 1
            } else {
                this.cisloFotky[0] += 1
            }
        },
        fotoMinus() {
            if (this.cisloFotky[0] === 1) {
                this.cisloFotky[0] = this.cisloFotky[1]
            } else {
                this.cisloFotky[0] -= 1
            }
        }
    }
}
</script>

<style scoped>
.nakup {
    padding: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
}

#container {
    display: flex;
    margin: 0 8vw;
    gap: 25px;
    justify-content: center;
    min-height: 32em;
}

#text {
    display: flex;
    flex-direction: column;
    width: 50%;
    align-items: center;
    justify-content: center;
    gap: 15px;
}

#fotky {
    width: 40%;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

.obrazek {
    width: 100%;
}

p {
    text-align: left;
}

.sipka {
    width: 10%;
    position: absolute;
    top: 45%;
}

#sipka1 {
    left: 0;
}

#sipka2 {
    right: 0;
}

#koupit {
    display: flex;
    gap: 40px;
    align-items: center;
}

</style>