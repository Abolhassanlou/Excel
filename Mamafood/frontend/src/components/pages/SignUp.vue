<template>
    <div v-if="isOpen" class="glass-container">
      <div class="glass-box">
        <button class="close-btn" @click="closeModal">×</button>
        <form @submit.prevent="register">
          <h1>Registrieren</h1>
          <input v-model="name" type="text" placeholder="Name" required>
          <input v-model="email" type="email" placeholder="E-Mail" required>
          <input v-model="password" type="password" placeholder="Password" required>
          <input v-model="confirmPassword" type="password" placeholder="Password wiederholen" required>
          <p v-if="passwordMismatch" class="error-message">Passwörter stimmen nicht überein!</p>
  
          <!--Password Policy Message-->
          <p class="password-policy">
            Ihr Passwort muss mindestens 7 Zeichen lang sein, mindestens einen Großbuchstaben, eine Zahl und ein Sonderzeichen enthalten.
          </p>
  
          <button type="submit" class="btn">Registrieren</button>
        </form>
        <p class="login-link">Schon ein Konto? <router-link to="/login">Hier einloggen</router-link></p>
      </div>
    </div>
  </template>
  
  <script>
  
  import axios from 'axios'
  export default {
    name: "SignUp",
    data() {
      return {
        isOpen: true,
        name: "",
        email: "",
        password: "",
        confirmPassword: ""
      };
    },
    computed: {
      passwordMismatch() {
        return this.password && this.confirmPassword && this.password !== this.confirmPassword;
      }
    },
    methods: {
    async register() {
      if (this.passwordMismatch) {
        alert("Passwörter stimmen nicht überein!");
        return;
      }
  
      try {
        // Send registration request to the backend
        const response = await axios.post("http://127.0.0.1:8000/users", {
          name: this.name,
          email: this.email,
          password: this.password
        });
  
        if (response.status === 201) {
          alert("Registrierung erfolgreich! please check your email");
          this.$router.push({name:'email-confirmation'});
          this.closeModal(); // Close modal on successful registration
        }
      } catch (error) {
        console.error("Registration failed:", error);
        alert("Fehler bei der Registrierung. Bitte versuchen Sie es später noch einmal.");
      }
    },
  
    closeModal() {
      this.isOpen = false;  // Modal wird geschlossen
    }
  }
    
    
  };
  </script>
  <style lang="scss" scoped>
 @use "@/assets/_button.scss" as *;

.glass-container {
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; // Damit das Modal in der Mitte bleibt

  .glass-box {
    position: relative; // Wichtig für .close-btn
    background: rgba(255, 250, 240, 0.8);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    width: 100%;
    border: 1px solid rgba(255, 255, 255, 0.3);
    margin: auto;
    margin-top: 40px;

    h1 {
      font-size: 35px;
      color: #4D331F;
      margin-bottom: 20px;
    }

    input {
      width: 100%;
      padding: 12px 20px;
      margin-bottom: 15px; // Statt 30px für besseres Design
      border: 1px solid rgba(255, 255, 255, 0.5);
      border-radius: 8px;
      font-size: 16px;
      background: rgba(255, 255, 255, 0.4);
      color: #4D331F;
      outline: none;
      transition: all 0.3s ease-in-out;

      &::placeholder {
        color: rgba(77, 51, 31, 0.7);
      }

      &:focus {
        border-color: #ffba58;
        box-shadow: 0 0 10px rgba(255, 186, 88, 0.5);
      }
    }

    .btn {
      @extend button;
      margin-top: 15px;
      width: 100%; // Damit es nicht schmal ist
    }

    .login-link {
      margin-top: 10px;
      color: #ffba58; /* Standardfarbe */
      text-decoration: none;
      transition: color 0.3s ease;
    }
    .login-link a:hover {
     color: #4A90E2; 
    }
    

    .close-btn {
      position: absolute;
      top: 15px;
      right: 20px;
      background: none;
      border: none;
      font-size: 24px;
      color: #333;
      cursor: pointer;
      transition: 0.3s;
    }

    .close-btn:hover {
      color: red;
    }

    .password-policy {
      color: #888; 
      font-size: 14px; 
      line-height: 1.5; 
      margin-top: 10px; 
      font-family: Arial, sans-serif; 
      padding: 5px 0;
    }

  }
}

  
  </style>