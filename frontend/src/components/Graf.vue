<template>
    <div class="grafDiv">
        <h3>{{jmeno}}</h3>
        <canvas class="graf" ref="graf"></canvas>
    </div>
</template>

<script>
// zobrazení grafu pomocí https://chartjs.org/
import Chart from 'chart.js/auto';

export default {
    name: "Graf",
    props: {
        graf: Array,
        labels: Array,
        jmeno: String,
        barva: String
    },
    mounted() {
        // globální settings
        Chart.defaults.elements.line.cubicInterpolationMode = 'monotone';
        Chart.defaults.plugins.legend.display = false

        let jmeno = this.jmeno
        const grafik = new Chart(this.$refs.graf, {
            type: this.graf[2],
            data: {
                datasets: [{
                    data: this.graf[1],
                    backgroundColor: this.barva + '70',
                    borderColor: this.barva
                }],
                labels: this.labels
            },
            options: {
                elements: {
                    point: {
                        radius: 5,
                        hitRadius: 15,
                        hoverRadius: 7
                    }
                },
                plugins: {
                    tooltip: {
                        // backgroundColor: '#000'
                        callbacks: {
                            label: function (context) {
                                let hodnota = context.dataset.label || '' + Math.round(context.parsed.y * 100) / 100
                                if (jmeno === 'Teplota') return hodnota + ' °C';
                                else if (jmeno === 'Vlhkost') return hodnota + ' %'
                                else if (jmeno === 'Tlak') return hodnota + ' hPa'
                                else if (jmeno === 'Vítr') return hodnota + ' m/s'
                                else if (jmeno === 'Srážky') return hodnota + ' mm/h'
                            }
                        }
                    },

                }
            }
        })
    }
}
</script>

<style scoped>
.graf {
    width: 100% !important;
    height: 100% !important;
}
.grafDiv {
    width: 40em;
    text-align: center;
    height: 100%;
}

.grafDiv h3 {
    margin-bottom: 10px;
}

</style>