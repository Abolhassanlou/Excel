<template>
  <div v-if="isOpen" class="glass-container">
    <div class="glass-box">
      <button class="close-btn" @click="closeModal">×</button>
      <div class="forgot-password">
        <h2>Passwort vergessen?</h2>
        <p>Bitte geben Sie Ihre E-Mail-Adresse ein, um Ihr Passwort zurückzusetzen.</p>

        <input v-model="email" type="email" placeholder="Ihre E-Mail-Adresse" required />

        <button class="btn" @click="sendResetLink">Passwort zurücksetzen</button>

        <p v-if="message" class="success">{{ message }}</p>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/utils/axios';

export default {
  data() {
    return {
      email: "",
      message: "",
      errorMessage: "",
      isOpen: true,
    };
  },
  methods: {
    async sendResetLink() {
      try {
        const response = await api.post('/auth/forgot-password', {
          email: this.email,
        });
        this.message = 'Überprüfen Sie Ihre E-Mails, um Ihr Passwort zurückzusetzen.';
        this.errorMessage = ""; // Clear any previous error
      } catch (err) {
        console.error('Error sending reset email:', err);
        if (err.response && err.response.data && err.response.data.message) {
          this.errorMessage = err.response.data.message;
        } else {
          this.errorMessage = 'Fehler beim Senden der E-Mail. Bitte versuche es später noch einmal.';
        }
        this.message = ""; // clear success message.
      }
    },
    closeModal() {
      this.isOpen = false;
    },
  },
};
</script>

<style lang="scss" scoped>
@use '@/assets/_button.scss' as *;

.glass-container {
  text-align: center;
  display: flex;

  .glass-box {
    position: relative;
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

    h2 {
      font-size: 24px;
      color: #4d331f;
      margin-bottom: 10px;
    }

    input {
      width: 100%;
      padding: 12px;
      margin-bottom: 20px;
      border: 1px solid rgba(255, 255, 255, 0.5);
      border-radius: 8px;
      font-size: 16px;
      background: rgba(255, 255, 255, 0.4);
      color: #4d331f;
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
      cursor: pointer;
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
  }

  .success{
    color: green;
  }
  .error{
    color: red;
  }
}
</style>