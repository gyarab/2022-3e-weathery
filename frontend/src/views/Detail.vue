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
                <apexchart id="graf" width="800" height="450px" type="area" :options="chartOptions" :series="series"></apexchart>
                <div id="milan">    
                    <h2><label for="change_date_btn">Choose time range:</label></h2>
                    <select id="change_date_btn" v-model="input_selected" @click="zmenaCasovehoRozmezi(input_selected)">
                        <option value="week">week</option>
                        <option value="month">month</option>
                        <option value="year">year</option>
                    </select>
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
                WindDirection: ['winddirection', '#00FF51', 'smer_vetru.png'],
                Rain: ['rain', '#0093FF', 'dest.png']
            },
            casoveRozmezi: 7, // dní - default
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
                console.log(this.data[i].pressure /= 100) // aby jsme to měli v hPa
            }

            this.zmenaAktivnihoGrafu(this.aktivniGraf)
            this.zmenaCasovehoRozmezi(this.selected)
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
        },
        zmenaCasovehoRozmezi(selected){
            this.aktivniRozmezi = selected
            let now = new Date() // dnešek
            if (selected == "week") {
                    this.casoveRozmezi = 7
                }
                else if (selected == "month") {
                    this.casoveRozmezi = 30
                }
                else if (selected == "year") {
                    this.casoveRozmezi = 365
                }
            now.setDate(now.getDate() - this.casoveRozmezi + 1)
            axios.get("/stats/" + this.souradnice[0] + "_" + this.souradnice[1], {
                params: {
                    date_from: `${now.getDate()}-${now.getMonth() + 1}-${now.getFullYear()}`,
                    date_to: 'now'
                }
            }).then(response => {
                this.data = response.data.data
                this.zmenaAktivnihoGrafu(this.aktivniGraf)
                
            })
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
    margin-left: 45%;
    background-color: var(--tmava);
    width: 80px;
    height: 35px;
    border-radius: 12px;
    border: none;
}
#milan{
    display: flex;
    justify-content: space-around;
    margin: 0;
    padding: 0;
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
</style>