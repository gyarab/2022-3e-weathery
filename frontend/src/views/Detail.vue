<template>
    <div id="detail">
        <h1>{{ souradnice[0] }} {{ souradnice[1] }}</h1>

        <div id="content">
            <div id="menicko">
                <button class="tlacitkoPrepinani" v-for="jmenoGrafu in Object.keys(grafy)" @click="aktivniGraf = jmenoGrafu">
                    {{ jmenoGrafu }}
                </button>
            </div>

            <Line v-if="grafData !== null" :data="grafData" :options="options"/>
            {{ aktivniGraf }}
        </div>
    </div>
</template>

<script>
import axios from "axios";
import {Line} from 'vue-chartjs'
import {Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
    name: "Detail",
    components: {Line},
    data() {
        return {
            grafy: {"Teplota": ['#ff0000', 'jmenoSouboru'], "Vlhkost": ['#003dff', 'jmenoSouboru']},
            aktivniGraf: "Teplota",
            souradnice: this.$route.params.souradnice.replaceAll(',', '.').split('-'),
            data: null,
            grafData: null,
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
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
                this.data = response.data.data
                console.log(this.data)

                this.grafData = {
                    labels: [],
                    datasets: []
                }

                for (let i in this.data[0]) {
                    console.log(this.data[0][i])
                    this.grafData.labels.push()
                }

                // {
                //     label: this.aktivniGraf,
                //     backgroundColor: this.grafy[this.aktivniGraf],
                //     data: []
                // }
            })

        // zobrazení grafu pomocí https://vue-chartjs.org/
    }
}
</script>

<style scoped>
#detail {
    padding: 10px;
}

#content {
    display: flex;
}

#menicko {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.tlacitkoPrepinani {
    padding: 30px;
    border: 1px solid;
    background-color: white;
}
</style>