<template>
  <div class="glass-container">
    <div class="glass-box">
      <h2>Reset Password</h2>
      <form @submit.prevent="resetPassword">
        <input type="password" id="newPassword" v-model="newPassword" placeholder="New Password" required />
        <input type="password" id="confirmPassword" v-model="confirmPassword" placeholder="Confirm Password" required />
        <button type="submit" class="btn">Reset Password</button>
      </form>
      <div v-if="message" :class="messageClass">
        <p>{{ message }}</p>
        <ul v-if="errorMessages.length">
          <li v-for="error in errorMessages" :key="error">{{ error }}</li>
        </ul>
      </div>
      <button v-if="resetSuccess" class="btn login-button" @click="goToLogin">Go to Login</button>
    </div>
  </div>
</template>

<script>
import api from '@/utils/axios';

export default {
  data() {
    return {
      newPassword: '',
      confirmPassword: '',
      message: '',
      errorMessages: [],
      resetSuccess: false,
      token: '',
      email: '',
    };
  },
  mounted() {
    const urlParams = new URLSearchParams(window.location.search);
    this.token = urlParams.get('token');
    this.email = urlParams.get('email');
  },
  computed: {
    messageClass() {
      return this.resetSuccess ? 'success' : 'error';
    },
  },
  methods: {
    async resetPassword() {
      if (this.newPassword !== this.confirmPassword) {
        this.message = 'Passwords do not match.';
        this.errorMessages = [];
        this.resetSuccess = false;
        return;
      }

      try {
        const response = await api.put('/auth/reset-password', {
          token: this.token,
          email: this.email,
          password: this.newPassword,
        });

        this.message = 'Password reset successful!';
        this.errorMessages = [];
        this.resetSuccess = true;
      } catch (error) {
        this.message = '';
        this.errorMessages = [];
        this.resetSuccess = false;

        if (error.response && error.response.data) {
          if (Array.isArray(error.response.data)) {
            this.errorMessages = error.response.data.map((err) => err.detail);
          } else if (error.response.data.detail) {
            this.errorMessages.push(error.response.data.detail);
          } else {
            this.message = 'Password reset failed.';
          }
        } else {
          this.message = 'An unexpected error occurred.';
        }
      }
    },
    goToLogin() {
      window.location.href = '/login';
    },
  },
};
</script>

<style scoped lang="scss">
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
      font-size: 35px;
      color: #4d331f;
      margin-bottom: 20px;
    }

    input {
      width: 100%;
      padding: 12px 20px;
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
      margin-top: 15px;
      padding: 10px 20px;
      background-color: #ffba58;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }

    .forgot-password {
      margin-top: 10px;
      a {
        color: #ffba58;
        text-decoration: none;
      }
    }

    .signup-link {
      margin-top: 10px;
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
}
</style>