<template>
    <div id="detail">
        <h1>{{ souradnice[0] }}° S, {{ souradnice[1] }}° E</h1>

        <div id="content">
            <div id="menicko">
                <button class="tlacitkoPrepinani" :class="{aktivniTlacitko: aktivniGraf === jmenoGrafu}"
                        v-for="jmenoGrafu in Object.keys(grafy)"
                        @click="zmenaAktivnihoGrafu(jmenoGrafu)">
                    {{ jmenoGrafu }}
                </button>
            </div>

            <div id="grafContainer">
                <apexchart width="800" height="450px" type="line" :options="chartOptions" :series="series"></apexchart>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "Detail",
    data() {
        return {
            grafy: {
                Teplota: ['temperature', '#ff4d00', 'pathIcona'],
                Vlhkost: ['humidity', '#000dff', 'pathIcona'],
                Tlak: ['pressure', '#595959', 'pathIcona']
            },
            casoveRozmezi: 14, // dní
            aktivniGraf: "Teplota",
            souradnice: this.$route.params.souradnice.replaceAll(',', '.').split('-'),
            data: null,
            chartOptions: {
                chart: {
                    id: 1,
                    zoom: {
                        enabled: false
                    },
                    toolbar: {
                        show: false,
                    }
                },
                xaxis: {
                    categories: [],
                },
                stroke: {
                    curve: 'smooth'
                },
                colors: [''],
                dataLabels: {
                    enabled: true,
                    enabledOnSeries: ['series-1']
                },

            },
            series: [
                {
                    name: 'Teplota',
                    data: [],
                },
            ],

        }
    },
    mounted() {
        let now = new Date() // dnešek
        now.setDate(now.getDate() - this.casoveRozmezi) // týden zpátky
        axios.get("/stats/" + this.souradnice[0] + "_" + this.souradnice[1], {
            params: {
                date_from: `${now.getDate()}-${now.getMonth() + 1}-${now.getFullYear()}`,
                date_to: 'now'
            }
        }).then(response => {
            this.data = response.data.data

            for (let i in this.data) {
            }

            this.zmenaAktivnihoGrafu(this.aktivniGraf)
        })

        // zobrazení grafu pomocí https://vue-chartjs.org/
    }
    ,
    methods: {
        zmenaAktivnihoGrafu(noveAktivni) {
            this.aktivniGraf = noveAktivni
            this.series[0].data = []
            this.chartOptions.xaxis.categories = []
            for (let i in this.data) {
                this.series[0].data.push(Math.round(this.data[i][this.grafy[this.aktivniGraf][0]] * 10) / 10)
                this.chartOptions.xaxis.categories.push(this.data[i].time)
            }
            this.series[0].name = this.aktivniGraf
            ApexCharts.exec('1', 'updateOptions', {colors: [this.grafy[this.aktivniGraf][1]]})
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
    margin-top: 30px;
}

#menicko {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.tlacitkoPrepinani {
    padding: 30px;
    border: none;
    background-color: white;
}

#grafContainer {
    padding: 20px;
    box-shadow: 0px 0px 25px grey;
    position: relative;
    z-index: 1;
}

.aktivniTlacitko {
    box-shadow: 0px 0px 25px grey;
    position: relative;
    z-index: 1;
    transition: 0.2s;
    border-radius: 10px 0 0 10px;
}
</style>