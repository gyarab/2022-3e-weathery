<template>
    <div class="admin">
        <Login v-if="!prihlasen" @probehloPrihlaseni="prihlaseni"></Login>

        <div id="layout" v-else>
            <h1>Administrace</h1>
            <table id="tabulkaObjednavky" v-if="objednavky.length > 0">
                <tr>
                    <th v-for="jmenoSloupce in Object.keys(objednavky[0])">{{ jmenoSloupce }}</th>
                </tr>
                <tr class="objednavkyRadek" v-for="(radek, i) in objednavky">
                    <td v-for="(sloupec, j) in radek">
                        <span v-if="j === 'order_state'">
                            <select v-model="objednavky[i]['order_state']" @change="zmenaStavu(objednavky[i]['id'], objednavky[i]['order_state'])">
                                <option value="paid">Zaplaceno</option>
                                <option value="sent">Odesláno</option>
                            </select>
                        </span>
                        <span v-else>{{ sloupec }}</span>

                    </td>
                </tr>
            </table>
            <div id="sideBar">Ještě nic</div>
        </div>
    </div>
</template>

<script>
import Detail from "@/views/Detail.vue";
import Login from "@/components/Login.vue";
import axios from "axios";

export default {
    name: "AdminView",
    components: {Login},
    data() {
        return {
            prihlasen: false,
            objednavky: {},
            token: '',
        }
    },
    mounted() {
        let token = localStorage.getItem('token')
        if (token != null) {
            this.token = token
            this.getObjednavky()
            this.prihlasen = true
        }
    },
    methods: {
        prihlaseni() {
            this.prihlasen = true
        },
        getObjednavky() {
            // requestnu idcka objednavek
            axios.get('orders', {
                headers: {
                    'Authorization': `token ${this.token}`
                }
            }).then(response => {
                this.objednavky = response.data['orders']

                // pro kazdou objednavku requestnu jeji vsechno info
                for (let i in this.objednavky) {
                    axios.get('order/' + this.objednavky[i].id, {
                        headers: {
                            'Authorization': `token ${this.token}`
                        }
                    }).then(response => {
                        this.objednavky[i] = response.data.data
                        this.objednavky[i].date = this.objednavky[i].date.replace('T', ' ')
                    })
                }
            })
        },
        zmenaStavu(id, stav) {
            console.log(id)
            axios.post('/update/' + id, {
                headers: {
                    'Authorization': `token ${this.token}`
                },
                state: 1 ? stav === 'sent' : 0
            })
        }
    }
}
</script>

<style scoped>
.admin {
    padding: 10px;
    display: flex;
    justify-content: center;
}

.admin h1 {
    grid-area: nadpis;
}

#layout {
    display: grid;
    grid-template:
        'nadpis nadpis nadpis'
        'tabulka tabulka bar'
    ;
    justify-items: center;
}

#sideBar {
    grid-area: bar;
}

#tabulkaObjednavky {
    width: 100%;
    background-color: white;
    border-collapse: collapse;
    border-width: 1px;
    border-color: var(--modra);
    border-style: solid;
    font-family: Inter, sans-serif;
    grid-area: tabulka;
}

#tabulkaObjednavky th, #tabulkaObjednavky td {
    border-width: 1px;
    border-color: var(--modra);
    border-style: solid;
    padding: 5px;
    text-align: center;
}

#tabulkaObjednavky th {
    background-color: var(--modra);
    color: var(--bila);
    font-weight: 100;
}
</style>