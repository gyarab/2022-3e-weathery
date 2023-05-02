<template>
    <div class="about">
        <h1>This is an about page</h1>
        <br>
        <p>Sem napíšem jak jsme to hezky udělali</p>
    </div>
</template>
<script>
export default {
    name: "About",
    mounted() {
    }
}

</script>

<style scoped>
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
}
</style>