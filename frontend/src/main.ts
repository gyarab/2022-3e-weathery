import { createApp} from 'vue'
import App from './App.vue'
import router from './router'

import './assets/styly.css'

const app = createApp(App)

app.use(router)

import axios from "axios";
axios.defaults.baseURL = "nejaky_URL_kde_to_salat_hostne";

app.mount('#app')