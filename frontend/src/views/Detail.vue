<template>
    <div id="detail">
        <h2 id="souradnice_stanice">{{ souradnice[0] }}° N, {{ souradnice[1] }}° E</h2>
        <div id="casoveObdobi">
            <h3>Časový interval</h3>
            <select class="prepinaniCasu" v-model="casoveRozmezi">
                <option value="7">Týden</option>
                <option value="14">2 týdny</option>
                <option value="30">Měsíc</option>
                <option value="182">Půl roku</option>
                <option value="365">Rok</option>
                <option value="730">2 roky</option>
                <option value="730">- Vlastní -</option>
            </select>
        </div>
        <div id="content">
            <Graf v-if="labels.length" v-for="graf in grafy" :graf="graf" :labels="labels" :jmeno="'JMENO'"></Graf>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import Graf from "@/components/Graf.vue";

export default {
    name: "Detail",
    components: {Graf},
    data() {
        return {
            grafy: {
                Teplota: ['temperature', [], 'line', '#ff0000'],
                Vlhkost: ['humidity', [], 'line', '#000dff'],
                Tlak: ['pressure', [], 'line', '#595959'],
                WindSpeed: ['wind_speed', [], 'line', '#00FFEC'],
                Rain: ['rain', [], 'line', '#0093FF']
            },
            data: {},
            souradnice: this.$route.params.souradnice.replaceAll(',', '.').split('-'),
            casoveRozmezi: 7,
            labels: [],
        }
    },
    async mounted() {
        let now = new Date() // dnešek
        now.setDate(now.getDate() - this.casoveRozmezi) // týden zpátky
        await this.requestData(now, 'now')

        for (let i in this.data) {
            this.data[i].pressure /= 100 // aby jsme to měli v hPa
        }

        for (let graf in this.grafy) { // nasazim hodnoty do this.grafy[1]
            let data = []
            for (let cas of this.data) {
                let udaj = cas[this.grafy[graf][0]]
                data.push(udaj)
            }
            this.grafy[graf][1] = data
        }

        for (let cas in this.data) {
            this.labels.push(this.data[cas].time)
        }
    },
    methods: {
        async requestData(datum_od, datum_do) {
            await axios.get("/stats/" + this.souradnice[0] + "_" + this.souradnice[1], {
                params: {
                    date_from: `${datum_od.getDate()}-${datum_od.getMonth() + 1}-${datum_od.getFullYear()}`,
                    date_to: datum_do
                }
            }).then(response => {
                if (response.data.message === "station does not exist") {
                    console.log("station does not exist") //TODO
                    this.$router.push('/')
                } else {
                    this.data = response.data.data
                }
            })
        },
        zmenaCasovehoRozmezi(selected) {
            let now = new Date() // dnešek
            if (selected === "day") {
                this.casoveRozmezi = 0.9
                this.custom_selected = false
            } else if (selected === "week") {
                this.casoveRozmezi = 7
                this.custom_selected = false
            } else if (selected === "month") {
                this.casoveRozmezi = 30
                this.custom_selected = false
            } else if (selected === "year") {
                this.casoveRozmezi = 365
                this.custom_selected = false
            } else if (selected === "custom") {
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
                })
            }
        },
        customZmena() {
            if ((this.cstm_date_from && this.cstm_date_to) !== null) {
                let a = this.cstm_date_from.split('-')
                let b = this.cstm_date_to.split('-')
                let a_date = new Date(`${a[1]}/${a[2]}/${a[0]}`) //měsíc, den, rok, aby fungovala metoda getTime()
                let b_date = new Date(`${b[1]}/${b[2]}/${b[0]}`)
                let date_diff = ((b_date.getTime() - a_date.getTime()) / 86400000) //rozdíl dat ve dnech
                let freq = null
                if (date_diff <= 1) { //3 - hodiny, 4 - dny, 5 - týdny, 6 - 14 dní, 7 - měsíce
                    freq = 3
                } else if (date_diff <= 50) {
                    freq = 4
                } else if (date_diff <= 365) {
                    freq = 5
                } else if (date_diff <= 365 * 2) {
                    freq = 6
                } else {
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

#souradnice_stanice {
    display: flex;
    justify-content: center;
    font-size: 30px;
}

#content {
    display: grid;
    grid-template-columns: auto auto;
    margin-top: 5px;
    align-self: center;
    width: 100%;
    justify-items: center;
    grid-gap: 40px;
}

.prepinaniCasu {
    width: 80px;
    height: 50px;
    background-color: white;
    border: none;
    outline: none;
}

#change_date_btn {
    display: flex;
    background-color: var(--bila);
    margin-left: 30px;
    width: 80px;
    height: 35px;
    border-radius: 5px;
    border: none;
}
</style>