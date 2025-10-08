<script>
import { useRoute } from 'vue-router';
import Navigation from '@/components/TheNavigation.vue';

export default {
  name: "App",
  components: {
    Navigation,
  },
  setup() {
    const route = useRoute();
    return { route };
  },
};
</script>

<template>
 <v-app>
    <div id="app">
      <!-- Navigation nur anzeigen, wenn showNav auf true gesetzt ist -->
    <Navigation v-if="route.meta.showNav" />  
    <router-view></router-view>  <!-- Wichtig: Zeigt die aktive Seite an -->
   
    </div>
 </v-app>
</template>