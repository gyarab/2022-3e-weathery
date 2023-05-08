import { createApp } from 'vue'
import '@/styly.css'
import App from '@/App.vue'
import router from "@/router.js";
import axios from "axios";

axios.defaults.baseURL = "https://api.weathery.svs.gyarab.cz/";

createApp(App)
    .use(router)
    .mount('#app')
