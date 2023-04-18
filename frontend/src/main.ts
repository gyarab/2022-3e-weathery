import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import axios from "axios";

import './assets/styly.css'

const app = createApp(App)

app.use(router)

axios.defaults.baseURL = "https://api.weathery.svs.gyarab.cz/";

app.mount('#app')