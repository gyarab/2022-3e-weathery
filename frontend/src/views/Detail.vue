<template>
    <p>tady budou ty grafiky</p>
    <br>
    {{souradnice}}
</template>

<script>
export default {
    name: "Detail",
    data() {
        return {
            souradnice: this.$route.params.souradnice.replaceAll(',', '.').split('-')
        }
    },
    mounted() {
        // request axios o data
        // zobrazení grafu pomocí https://vue-chartjs.org/
    }
}
</script>

<style scoped>

</style>