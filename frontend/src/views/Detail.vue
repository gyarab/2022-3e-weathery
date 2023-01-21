<template>
    <div id="detail">

        <div id="content">
            <div id="menicko">
                <button v-for="jmenoGrafu in Object.keys(grafy)" class="tlacitkoPrepinani" :class="{aktivniTlacitko: aktivniGraf === jmenoGrafu}"
                        @click="zmenaAktivnihoGrafu(jmenoGrafu)">
                    {{ jmenoGrafu }}
                </button>
            </div>

            <div id="grafContainer">
                <apexchart id="graf" width="800" height="450px" type="area" :options="chartOptions" :series="series"></apexchart>
                <h2>{{ souradnice[0] }}° S, {{ souradnice[1] }}° E</h2>
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
                Teplota: ['temperature', '#ff0000', ''],
                Vlhkost: ['humidity', '#000dff', ],
                Tlak: ['pressure', '#595959', 'pathIcona'],
                WindSpeed: ['windspeed', '#00FFEC' , 'pathIcona'],
                WindDirection: ['Winddirection', '#00FF51', 'pathIcona'],
                Rain: ['rain', '#0093FF', '3']
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
                    },
                    background: '#AAC4FF'
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
                console.log(this.data[i].pressure /= 100) // aby jsme to měli v hPa
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
    padding: 20px;
    display: flex;
    flex-direction: column;
}

#content {
    display: flex;
    margin-top: 5px;
    align-self: center;
}

#menicko {
    display: flex;
    flex-direction: column;
    gap: 5px;
    align-items: end;
}

#grafContainer {
    padding: 20px;
    border-radius: 5px;
    z-index: 3;
    background-color: var(--svetla);
}

#graf {
    border-radius: 5px;
}

.tlacitkoPrepinani {
    padding: 20px 20px 20px 0;
    background-color: var(--svetla);
    border-radius: 5px 0 0 5px;
    left: 20px;
    position: relative;
    width: 80px;
    border: none;
    transition: 0.2s;
    margin-left: 34px;
}

.aktivniTlacitko {
    width: 100px;
    transition: 1s;
    border-right: none;
    background-color: var(--tmava);
    z-index: 4;
    margin-left: 0;
}
</style>