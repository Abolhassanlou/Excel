<template>
    <div class="confirmation-container">
      <div class="confirmation-box">
        <h1>Registrierung abgeschlossen!</h1>
        <p>Bitte überprüfen Sie Ihre E-Mail und klicken Sie auf den Bestätigungslink, um Ihr Konto zu aktivieren.</p>
        <p>Nach der Aktivierung können Sie sich einloggen.</p>
        <router-link to="/login" class="btn">Zur Login-Seite</router-link>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "EmailConfirmation"
  };
  </script>
  
  <style scoped>
  .confirmation-container {
    text-align: center;
    padding: 20px;
  }
  
  .confirmation-box {
    background: rgba(255, 250, 240, 0.8);
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
    margin: auto;
    margin-top: 40px;
  }
  
  .confirmation-box h1 {
    font-size: 24px;
    color: #4D331F;
    margin-bottom: 20px;
  }
  
  .confirmation-box p {
    font-size: 16px;
    color: #4D331F;
  }
  
  .btn {
    display: inline-block;
    padding: 10px 20px;
    margin-top: 20px;
    background-color: #ffba58;
    color: white;
    border-radius: 5px;
    text-decoration: none;
  }
  </style>
  