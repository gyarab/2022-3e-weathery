<template>
    <p>tady budou ty grafiky</p>
    <br>
    {{ souradnice }}
    {{ data }}
</template>

<script>
import axios from "axios";

export default {
    name: "Detail",
    data() {
        return {
            souradnice: this.$route.params.souradnice.replaceAll(',', '.').split('-'),
            data: null
        }
    },
    mounted() {
        // request axios o data
        let now = new Date() // dnešek
        now.setDate(now.getDate() - 7) // týden zpátky
        axios.get("/stats/" + this.souradnice[0] + "_" + this.souradnice[1], {
            params: {
                date_from: `${now.getDate()}-${now.getMonth() + 1}-${now.getFullYear()}`,
                date_to: "now"
            }
        })
            .then(response => {
                this.data = response.data

            })

        // zobrazení grafu pomocí https://vue-chartjs.org/
    }
}
</script>

<style scoped>

</style>