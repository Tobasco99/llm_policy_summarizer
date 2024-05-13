import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/aura-light-green/theme.css'
import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'

import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'
import Slider from 'primevue/slider'
import Sidebar from 'primevue/sidebar';
import FloatLabel from 'primevue/floatlabel';

import App from './App.vue'
import router from './router'
import { defaultLocale, languages } from './i18n/index'

const i18n = createI18n({
  legacy: false,
    locale: defaultLocale,
    messages: Object.assign(languages)
  })

const app = createApp(App)

app.use(createPinia())
app.use(i18n)
app.use(PrimeVue)

app.component('InputText', InputText)
app.component('Button', Button)
app.component('Dropdown', Dropdown)
app.component('Slider', Slider)
app.component('Sidebar', Sidebar)
app.component('FloatLabel', FloatLabel)

app.use(router)

app.mount('#app')
