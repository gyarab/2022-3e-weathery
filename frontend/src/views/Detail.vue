<template>
    <div id="detail">
        <h2 id="souradnice_stanice">{{ souradnice[0] }}° N, {{ souradnice[1] }}° E</h2>
        <div id="casovyInterval">
            <h3>Časový interval:</h3>
            <select class="prepinaniCasu" v-model="casoveRozmezi" @change="zmenaCasovehoRozmezi">
                <option value="1">Den</option>
                <option value="7">Týden</option>
                <option value="14">2 týdny</option>
                <option value="30">Měsíc</option>
                <option value="182">Půl roku</option>
                <option value="365">Rok</option>
                <option value="730">2 roky</option>
                <option value="0">- Vlastní -</option>
            </select>
        </div>
        <div v-if="casoveRozmezi === '0'" id="customInterval">
            <input type="date"> -
            <input type="date">
        </div>
        <div id="content">
            <Graf v-if="labels.length" v-for="(graf, index) in grafy" :graf="graf" :labels="labels" :jmeno="Object.keys(grafy).find(key => grafy[key] === graf)" :key="forceRefresh + index"></Graf>
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
                Vítr: ['wind_speed', [], 'line', '#00FFEC'],
                Déšť: ['rain', [], 'line', '#0093FF']
            },
            data: {},
            souradnice: this.$route.params.souradnice.replaceAll(',', '.').split('-'),
            casoveRozmezi: 14,
            labels: [],
            forceRefresh: 0
        }
    },
    async mounted() {
        let datum = new Date() // dnešek
        datum.setDate(datum.getDate() - parseInt(this.casoveRozmezi)) // týden zpátky
        await this.requestData(datum, 'now')
        this.formatDat()
    },
    methods: {
        async requestData(datum_od, datum_do) {
            await axios.get("/stats/" + this.souradnice[0] + "_" + this.souradnice[1], {
                params: {
                    date_from: datum_od === 'day_ago' ? 'day_ago': `${datum_od.getDate()}-${datum_od.getMonth() + 1}-${datum_od.getFullYear()}`,
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
        formatDat() {
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
            if (this.casoveRozmezi === '1') {
                this.labels = [] // upravim osu x jakoby (novy datumy)
                for (let cas in this.data) {
                    this.labels.push(this.data[cas].time.slice(11, 14) + '00')
                    console.log(this.labels[cas])

                    if (this.labels[cas] === '22:00') this.labels[cas] = '00:00'
                    else if (this.labels[cas] === '23:00') this.labels[cas] = '01:00'
                    else {
                        this.labels[cas] = parseInt(this.labels[cas].slice(0, 3)) + 2 + ':00'
                        if (this.labels[cas].length === 4) this.labels[cas] = '0' + this.labels[cas]
                    }
                }
            } else {
                this.labels = [] // upravim osu x jakoby (novy datumy)
                for (let cas in this.data) {
                    this.labels.push(this.data[cas].time.slice(0, 10).replaceAll('-', '. '))
                }
            }

        },
        async zmenaCasovehoRozmezi() {
            if (this.casoveRozmezi !== '0') {
                let datum = new Date() // dnešek
                datum.setDate(datum.getDate() - parseInt(this.casoveRozmezi))
                if (this.casoveRozmezi === '1') {
                    await this.requestData('day_ago', 'now')
                } else {
                    await this.requestData(datum, 'now')
                }
                this.formatDat()
                this.forceRefresh += 1
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
    font-family: Inter, sans-serif;
    align-items: center;
}

#souradnice_stanice {
    display: flex;
    justify-content: center;
    font-size: 30px;
}

#casovyInterval {
    display: flex;
    justify-content: center;
    gap: 10px;
    align-items: center;
}

#content {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 5em;
    width: 100%;
    margin-top: 3em;
}

.prepinaniCasu {
    width: auto ;
    height: 30px;
    background-color: var(--bila);
    border: none;
    outline: none;
    font-family: Inter, sans-serif;
    font-weight: bold;
    font-size: 1em;
    cursor: pointer;
}

.prepinaniCasu::after {
}

#customInterval {

}

input[type="date"] {
    padding: 3px;
    font-size: 14px;
    outline: none;
    border-radius: 5px;
    border: none;
    font-family: inherit;
}

::-webkit-calendar-picker-indicator {
    padding: 5px;
    cursor: pointer;
    border-radius: 3px;
}
</style>