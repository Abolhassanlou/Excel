<!-- src/views/Login.vue -->
<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="loginUser">
      <input
        type="email"
        v-model="email"
        placeholder="Email"
        required
      />
      <input
        type="password"
        v-model="password"
        placeholder="Password"
        required
      />
      <button type="submit">Login</button>
    </form>
    <p>
      Don't have an account? <router-link to="/signup">Sign Up</router-link>
    </p>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'; // Adjust path if needed

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    async loginUser() {
      const authStore = useAuthStore();
      try {
        await authStore.login(this.email, this.password);
        // After successful login, navigate to a protected or home page:
        this.$router.push('/protected'); 
      } catch (error) {
        alert(error.message);
      }
    },
  },
};
</script>

<style scoped>
/* Optional styles */
</style>
