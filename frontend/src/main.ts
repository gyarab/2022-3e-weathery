import { createApp} from 'vue'
import App from './App.vue'
import router from './router'
import VueApexCharts from "vue3-apexcharts";

import './assets/styly.css'

const app = createApp(App)
app.use(VueApexCharts);


app.use(router)

import axios from "axios";
axios.defaults.baseURL = "https://weathery.svs.gyarab.cz/api";

app.mount('#app')