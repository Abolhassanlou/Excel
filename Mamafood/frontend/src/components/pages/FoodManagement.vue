<template>
    <div>
      <h1>Food Management</h1>
      <p>Verwalte deine Lebensmittel hier:</p>
      
      <!-- Hier kannst du zum Beispiel eine Liste von Lebensmitteln anzeigen und eine Funktion zum Hinzufügen/Ändern/Löschen von Lebensmitteln einbauen -->
      <div>
        <ul>
          <li v-for="food in foods" :key="food.id">{{ food.name }}</li>
        </ul>
      </div>
  
      <!-- Formular für Hinzufügen von Lebensmittel -->
      <form @submit.prevent="addFood">
        <input v-model="newFoodName" type="text" placeholder="Name des Lebensmittels" />
        <button type="submit">Hinzufügen</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        foods: [],  // Liste der Lebensmittel
        newFoodName: "",  // Eingabe für neues Lebensmittel
      };
    },
    methods: {
      addFood() {
        if (this.newFoodName) {
          this.foods.push({ id: Date.now(), name: this.newFoodName });
          this.newFoodName = "";  // Eingabefeld zurücksetzen
        }
      },
    },
  };
  </script>
  