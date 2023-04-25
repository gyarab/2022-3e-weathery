<template>
    <div>
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
        jmeno: String
    },
    mounted() {
        // globální settings
        Chart.defaults.elements.line.cubicInterpolationMode = 'monotone';
        Chart.defaults.plugins.legend.display = false

        const grafik = new Chart(this.$refs.graf, {
            type: this.graf[2],
            data: {
                datasets: [{
                    data: this.graf[1],
                }],
                labels: this.labels
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: this.jmeno
                    }
                }
            }
        });
    }
}
</script>

<style scoped>
.graf {
    width: 100% !important;
    height: 100% !important;
}
</style>