import { createApp } from 'vue';
import App from './App.vue';
import { createPinia } from 'pinia';  // Import Pinia
import router from './router';  // Import your router (if you're using one)

const app = createApp(App);

// Create Pinia store instance
const pinia = createPinia();

// Use Pinia store and router in the app
app.use(pinia);
app.use(router);  // Ensure you use router if you're using Vue Router

app.mount('#app');
