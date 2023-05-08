<template>
    <div class="about">
        <h1>Co je Weathery?</h1>
        <br>
        <p>Je to studentský projekt vytvořený jako ročníková práce ve 3. ročníku na Gymnáziu, Arabská 14. Cílem projektu je vytvořit prototyp meterologické stanice, backend
            starající se o servírování dat ze stanice a tuto webovou aplikaci na sledování dlouhodobých dat co se počasí týče. <br><br>
            Více se můžete dozvědět v <a href="https://github.com/gyarab/2022-3e-weathery">Github Repozítáři</a>.</p>

    </div>
</template>
<script>
export default {
    name: "About",
}

</script>

<style scoped>
.about h1 {
    margin-bottom: 10px;
}

.about p {
    width: 60%;
    text-align: center;
}

.about {
    padding: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

@media only screen and (max-width: 1200px) {
    .about h1 {
        text-align: center;
    }

    .about p {
        width: 90%;
    }
}
</style>