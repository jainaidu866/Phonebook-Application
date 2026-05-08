import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'

axios.defaults.headers.common['ngrok-skip-browser-warning'] = 'true'

createApp(App).mount('#app')