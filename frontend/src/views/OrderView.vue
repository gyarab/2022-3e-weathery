<template>
    <div class="objednavka">
        <div class="udaje">
            <h2>Číslo objednávky:</h2>
            <h1>{{ data.id }}</h1>
            <h2>{{ datum }}</h2>

            <div class="konteiner">
                <h2>Místo doručení: </h2><h2>{{ data.street }} {{data.city}} {{data.postal_code}} {{data.country}}</h2>
                <h2>Adresát: </h2><h2>{{data.name}} ({{data.email}})</h2>
                <h2>Stav: </h2><h2>{{ stav }}</h2>
            </div>
        </div>        
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
        },
        stav() {
            return this.data.order_state == "sent" ? "Odesláno" : "Zaplaceno (Objednávka se zpracovává)"
        }
    }
}
</script>

<style scoped>
.objednavka {
    display: flex;
    justify-content: center;
}

.udaje {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 80%;
    text-align: center;
}

.konteiner {
    margin-top: 30px;
    display: grid;
    row-gap: 10px;
    column-gap: 30px;
    grid-template-columns: auto auto;
    justify-items: start;
}

</style>