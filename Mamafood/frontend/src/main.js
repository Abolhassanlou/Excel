import { createApp } from 'vue';
import App from './App.vue';

import router from './router';
import api from './utils/axios';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faUser } from '@fortawesome/free-solid-svg-icons';
// Bootstrap CSS und JS
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";

// BootstrapVueNext korrekt importieren
import * as BootstrapVueNext from "bootstrap-vue-next";
import "bootstrap-vue-next/dist/bootstrap-vue-next.css";
import '@fortawesome/fontawesome-free/css/all.css';

library.add(faUser);

const app = createApp(App);


app.use(router);
app.use(BootstrapVueNext);
app.config.globalProperties.$api = api;
 
app.component('font-awesome-icon', FontAwesomeIcon);
app.mount('#app');