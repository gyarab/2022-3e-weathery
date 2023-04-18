<template>
    <canvas id="graf" ref="graf"></canvas>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
    name: "Graf",
    props: {
        typ: String,
        data: {}
    },
    mounted() {
        const grafik = new Chart(this.$refs.graf, {
            type: this.typ,
            data: this.data
        });
    }
}
</script>

<style scoped>
#graf {
    width: 1000px;
}
</style>