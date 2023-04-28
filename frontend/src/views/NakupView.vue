<template>
    <div class="nakup">
        <h1>Weathery stanice v1</h1>

        <p>Domácí meterologická stanice se schopnostmi profesionálního stroje?
            To je naše Weathery stanice která dokáže měřit aktuální teplotu, srážky, rychlost a směr větru, tlak a vlhkost vzduchu.
            Všechna tyto data poté posílá na náš server kde se po registraci budou na příslušných souřadniciích zobrazovat naměřená data.
        </p>
        <img class="obrazek" src="@/assets/stanice0.jpg" alt="Fotka stanice 1">
        <p>Sem ještě něco pane Salát</p>
        <img class="obrazek" src="@/assets/stanice1.jpg" alt="Fotka stanice 2">
        <p>Sem ještě něco pane Salát</p>
        <button class="btn" onclick="window.location.href = 'https://buy.stripe.com/test_aEU4hqeOt0Freje288'">Koupit</button>
    </div>
</template>

<script>
export default {
    name: "NakupView"
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

.obrazek {
    width: 40%;
}

p {
    width: 80%;
    text-align: center;
}

</style>