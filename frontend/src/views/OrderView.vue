<template>
    <div class="objednavka">
        <h1>Číslo objednávky: {{ data.id }}</h1>
        <h2>Datum: {{ datum }}</h2>
        <h2>Místo doručení: {{ data.street }} {{data.city}} {{data.postal_code}} {{data.country}}</h2>
        <h2>Adresát: {{data.name}} ({{data.email}})</h2>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "OrderView",
    data() {
        return {
            data: {},
            order_id: this.$route.params.id,
        }
    },
    beforeMount() {
        axios.get("/order/" + this.order_id, {}).then(response => {
            this.data = response.data.data
        })
    },
    computed: {
        datum() {
            try {
                let list = this.data.date.replace('T', '-').split('-')
                return `${list[2]}.${list[1]}. ${list[0]}`
            }
            catch (e) {} //jeste jsme nedostali data

        }
    }
}
</script>

<style scoped>
.objednavka {
    padding: 10px
}
</style>