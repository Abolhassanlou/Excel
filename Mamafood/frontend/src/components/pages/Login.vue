<template>
  <div v-if="isOpen" class="glass-container">
    <div class="glass-box">
      <button class="close-btn" @click="closeModal">×</button>
      <h1>Login</h1>
      <form @submit.prevent="login">
        <input type="email" v-model="email" placeholder="Enter E-Mail" />
        <input type="password" v-model="password" placeholder="Enter Password" />
        <button class="btn" type="submit">Login</button>
        <p class="forgot-password">
          <router-link to="/forgot-password">Passwort vergessen?</router-link>
        </p>
        <p class="signup-link">
          No Account? <router-link to="/signup">Register Here</router-link>
        </p>
        <p v-if="loginError" class="error">{{ loginError }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { setUser } from '@/stores/auth'; // Assuming this sets user data in a store

const email = ref('');
const password = ref('');
const loginError = ref(null);
const router = useRouter();
const isOpen = ref(true); // Assuming this controls the modal visibility

const login = async () => {
  if (!email.value || !password.value) {
    loginError.value = 'Please fill in all fields!';
    return;
  }

  loginError.value = null; // Clear previous errors

  try {
    const params = new URLSearchParams();
    params.append('username', email.value);
    params.append('password', password.value);

    const response = await axios.post('http://127.0.0.1:8000/auth/login', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    const { access_token, refresh_token, expires_in } = response.data;

    // Store tokens immediately upon successful authentication
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    localStorage.setItem('expires_in', expires_in);

    const userResponse = await axios.get('http://127.0.0.1:8000/users/me', {
      headers: {
        Authorization: `Bearer ${access_token}`,
      },
    });

    const userData = userResponse.data;
    const role = userData.role;
    const isUserActive = userData.is_active; // Or userData.user_activated === 1 if it's a numeric flag

    // --- NEW LOGIC HERE ---
    if (!isUserActive) {
      // If the user is not active, display an error and try to resend the activation link
      loginError.value = 'Account not activated. A new activation email has been sent. Please check your inbox.';

      // Clear tokens as login wasn't fully successful (user not active)
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('expires_in');
      setUser(null); // Clear user from store
      
      return; // Stop the login process here
    }
    // --- END NEW LOGIC ---

    // If the user IS active, proceed with setting user and redirection
    setUser(userData); // Set user data in your Pinia/Vuex store

    // Redirect based on role
    if (role === 0) {
      router.push('/userdashboard');
    } else if (role === 1) {
      router.push('/chefinfo');
    } else {
      router.push('/userdashboard'); // Default redirect
    }

    closeModal(); // Close the login modal
  } catch (error) {
    console.error('Login failed:', error);
    // This catch block will now primarily handle issues like
    // invalid credentials (401), network errors, etc.
    if (error.response?.data?.detail) {
      loginError.value = error.response.data.detail;
    } else {
      loginError.value = 'Login failed. Please check your credentials and try again.';
    }
    setUser(null); // Ensure user is not set in store on any error
  }
};

const closeModal = () => {
  isOpen.value = false;
  router.push('/');
};
</script>


<style lang="scss" scoped>
@use '@/assets/_button.scss' as *;

.glass-container {
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;

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
    width: 90%;
    border: 1px solid rgba(255, 255, 255, 0.3);

    h1 {
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
      @extend button;
      margin-top: 15px;
    }

    .forgot-password,
    .signup-link {
      margin-top: 10px;
      a {
        color: #ffba58;
        text-decoration: none;
      }
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

      &:hover {
        color: red;
      }
    }

    .error {
      color: red;
      margin-top: 10px;
    }
  }
}
</style>
