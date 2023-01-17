<template>
    <div id="detail">
        <h1>{{ souradnice[0] }} {{ souradnice[1] }}</h1>

        <div id="content">
            <div id="menicko">
                <button class="tlacitkoPrepinani" v-for="jmenoGrafu in Object.keys(grafy)"
                        @click="zmenaAktivnihoGrafu(jmenoGrafu)">
                    {{ jmenoGrafu }}
                </button>
            </div>

            <Line v-if="grafData !== null" :data="grafData" :options="options"/>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import {Line} from 'vue-chartjs'
import {Chart as ChartJS, Title, Tooltip, PointElement, LineElement, CategoryScale, LinearScale} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip)

export default {
    name: "Detail",
    components: {Line},
    data() {
        return {
            grafy: {Teplota: ['temperature', '#ff4d00'], Vlhkost: ['humidity', '#000dff']},
            casoveRozmezi: "7", // dní
            aktivniGraf: "Teplota",
            souradnice: this.$route.params.souradnice.replaceAll(',', '.').split('-'),
            data: null,
            options: {
                responsive: true,
                maintainAspectRatio: false
            },
            grafData: null,
        }
    },
    mounted() {
        let now = new Date() // dnešek
        now.setDate(now.getDate() - 7) // týden zpátky
        axios.get("/stats/" + this.souradnice[0] + "_" + this.souradnice[1], {
            params: {
                date_from: `${now.getDate()}-${now.getMonth() + 1}-${now.getFullYear()}`,
                date_to: 'now'
            }
        }).then(response => {
            this.data = response.data.data

            this.zmenaAktivnihoGrafu(this.aktivniGraf)
        })

        // zobrazení grafu pomocí https://vue-chartjs.org/
    },
    methods: {
        zmenaAktivnihoGrafu(noveAktivni) {
            this.aktivniGraf = noveAktivni
            let grafData = {
                labels: [],
                datasets: [
                    {
                        backgroundColor: this.grafy[this.aktivniGraf][1],
                        data: [],
                    }
                ]
            }
            for (let i in this.data) {
                grafData.datasets[0].data.push(this.data[i][this.grafy[this.aktivniGraf][0]])
                grafData.labels.push(this.data[i].time)
            }
            this.grafData = grafData
        }
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

canvas {
    max-width: 1200px;
    height: 500px;
}
</style>