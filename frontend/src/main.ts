import { createApp} from 'vue'
import App from './App.vue'
import router from './router'

import './assets/styly.css'

const app = createApp(App)

app.use(router)

import axios from "axios";
axios.defaults.baseURL = "https://weathery.svs.gyarab.cz/api";

app.mount('#app')