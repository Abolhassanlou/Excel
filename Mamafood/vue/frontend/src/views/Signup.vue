<!-- src/views/Signup.vue -->
<template>
  <div>
    <h1>Signup</h1>
    <form @submit.prevent="signupUser">
      <input
        type="text"
        v-model="username"
        placeholder="Username"
        required
      />
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
      <button type="submit">Signup</button>
    </form>
    <p>
      Already have an account? <router-link to="/login">Login</router-link>
    </p>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  name: 'Signup',
  data() {
    return {
      username: '',
      email: '',
      password: '',
    };
  },
  methods: {
    async signupUser() {
      const authStore = useAuthStore();
      const success = await authStore.signup(this.username, this.email, this.password);
      if (success) {
        this.$router.push('/login');
      } else {
        alert('Signup failed.');
      }
    },
  },
};
</script>

<style scoped>
/* Optional styles */
</style>
