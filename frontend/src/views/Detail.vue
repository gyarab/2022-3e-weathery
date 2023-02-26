<template>
    <div id="detail">

        <div id="content">
            <div id="menicko">
                <button v-for="jmenoGrafu in Object.keys(grafy)" class="tlacitkoPrepinani" :class="{aktivniTlacitko: aktivniGraf === jmenoGrafu}"
                    @click="zmenaAktivnihoGrafu(jmenoGrafu)">
                    <img class="graf_ikonky" :src="'src/assets/icony/'+grafy[jmenoGrafu][2]">
                </button>
            </div>

            <div id="grafContainer">
                <apexchart id="graf" width="800" height="450px" :type="chart_type" :options="chartOptions" :series="series"></apexchart>
                <div>
                    <h2><label for="change_date_btn">Choose time range:</label></h2>
                    <select id="change_date_btn" v-model="input_selected" @click="zmenaCasovehoRozmezi(input_selected)">
                        <option value="week">week</option>
                        <option value="month">month</option>
                        <option value="year">year</option>
                        <option value="custom">custom</option>
                    </select>
                </div>
                <div v-if="custom_selected" id="dateContainer">
                    <input type="date" id="cstm_from" v-model="cstm_date_from" @change="customZmena()">
                    <input type="date" id="cstm_to" v-model="cstm_date_to" @change="customZmena()">
                </div>
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
                Teplota: ['temperature', '#ff0000', 'teplo.png'],
                Vlhkost: ['humidity', '#000dff', 'vlhkost.png'],
                Tlak: ['pressure', '#595959', 'tlak.png'],
                WindSpeed: ['windspeed', '#00FFEC' , 'rychlost_vetru.png'],
                Rain: ['rain', '#0093FF', 'dest.png']
            },
            casoveRozmezi: 7, // dní - default
            aktivniGraf: "Teplota",
            souradnice: this.$route.params.souradnice.replaceAll(',', '.').split('-'),
            data: null,
            custom_selected: false,
            cstm_date_from: null,
            cstm_date_to: null,
            chart_type: 'area', 
            chartOptions: {
                bar: {
                    borderRadius: 30
                },
                chart: {
                    id: 1,
                    zoom: {
                        enabled: false
                    },
                    toolbar: {
                        show: true,
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
                this.data[i].pressure /= 100 // aby jsme to měli v hPa
            }

            this.zmenaAktivnihoGrafu(this.aktivniGraf)
            this.zmenaCasovehoRozmezi(this.selected)
        })

        // zobrazení grafu pomocí https://apexcharts.com/
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

            if (noveAktivni == WindSpeed) { //chci dát na osu y hodnoty z widspeedu a podle barev linky rozlišovat směr větru
                this.chart_type = 'line'

            }
        },
        zmenaCasovehoRozmezi(selected){
            let now = new Date() // dnešek
            if (selected == "week") {
                    this.casoveRozmezi = 7
                    this.custom_selected = false
                }
                else if (selected == "month") {
                    this.casoveRozmezi = 30
                    this.custom_selected = false
                }
                else if (selected == "year") {
                    this.casoveRozmezi = 365
                    this.custom_selected = false
                }
                else if (selected == "custom") {
                    this.custom_selected = true
                }

            if (selected !== "custom") {
                now.setDate(now.getDate() - this.casoveRozmezi + 1)
                axios.get("/stats/" + this.souradnice[0] + "_" + this.souradnice[1], {
                    params: {
                        date_from: `${now.getDate()}-${now.getMonth() + 1}-${now.getFullYear()}`,
                        date_to: 'now',
                    }
                }).then(response => {
                    this.data = response.data.data
                    this.zmenaAktivnihoGrafu(this.aktivniGraf)
                    
                })
            }
        },
        customZmena() {
            if ((this.cstm_date_from && this.cstm_date_to) !== null) {
                var a = this.cstm_date_from.split('-')
                var b = this.cstm_date_to.split('-')
                var a_date = new Date(`${a[1]}/${a[2]}/${a[0]}`) //měsíc, den, rok, aby fungovala metoda getTime()
                var b_date = new Date(`${b[1]}/${b[2]}/${b[0]}`)
                var date_diff = ((b_date.getTime() - a_date.getTime())/86400000) //rozdíl dat ve dnech
                var freq = null
                if (date_diff <= 1){ //3 - hodiny, 4 - dny, 5 - týdny, 6 - 14 dní, 7 - měsíce
                    freq = 3
                }else if(date_diff <= 50){
                    freq = 4
                }else if (date_diff <= 365){
                    freq = 5
                }else if (date_diff <= 365*2) {
                    freq = 6
                }else{
                    freq = 7
                }
                axios.get("/stats/" + this.souradnice[0] + "_" + this.souradnice[1], {
                    params: {
                        date_from: `${a[2]}-${a[1]}-${a[0]}`,
                        date_to: `${b[2]}-${b[1]}-${b[0]}`,
                        freq: freq
                    }
                }).then(response => {
                    this.data = response.data.data
                    this.zmenaAktivnihoGrafu(this.aktivniGraf)
                })
            }
            
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
#change_date_btn{
    display: flex;
    background-color: var(--tmava);
    margin-left: 30px;
    width: 80px;
    height: 35px;
    border-radius: 12px;
    border: none;
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
.graf_ikonky {
    width: 30px;
    height: 30px;
}

#apexcharts1{
    border-radius: 5px;
}
</style>