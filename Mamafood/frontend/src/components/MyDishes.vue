<template>
    <div class="container">
      <h2 class="text-center mb-4">Mein Essen</h2>
  
      <!-- Grid für die Karten -->
      <div class="row">
        <div class="col-md-4" v-for="dish in dishes" :key="dish.id">
          <!-- Karte für jedes Gericht -->
          <div class="card" style="width: 18rem;">
            <img :src="dish.image_url" class="card-img-top" :alt="dish.food_name">
            <div class="card-body">
              <h5 class="card-title">{{ dish.food_name }}</h5>
              <p class="card-text">{{ dish.description }}</p>
              <p class="card-text"><strong>Preis:</strong> €{{ dish.price }}</p>
              <p class="card-text"><strong>Vorbereitungszeit:</strong> {{ dish.preparation_time }}</p>
              <a href="#" class="btn btn-primary">Mehr erfahren</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mockDataProvider } from "../services/MockDataProvider";
  
  export default {
    name: "MyDishes",
    data() {
      return {
        dishes: [], // Array für die Gerichte
      };
    },
    async created() {
      // Daten beim Erstellen der Komponente laden
      const dishes = await mockDataProvider.getDishes();
      this.dishes = dishes; // Zuweisen der Daten
    },
  };
  </script>
  
  <style scoped>
  /* Optional: Stil für die Karten oder den Container */
  .container {
    margin-top: 20px;
  }
  .card {
    margin-bottom: 20px;
  }
  </style>
  