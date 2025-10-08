<template>
    <div>
      <p v-if="loading">Verifying account...</p>
      <p v-if="verificationMessage">{{ verificationMessage }}</p>
      <p v-if="error">{{ error }}</p>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import axios from 'axios';
  
  const route = useRoute();
  const router=useRouter();
  const loading = ref(true);
  const verificationMessage = ref('');
  const error = ref('');
  
  onMounted(async () => {
    const token = route.query.token;
    const email = route.query.email;
  
    if (!token || !email) {
      error.value = 'Invalid verification link.';
      loading.value = false;
      return;
    }
  
    try {
      const response = await axios.post('http://127.0.0.1:8000/users/verify', { // Replace 8000 with your backend port
        token: token,
        email: email,
      });
  
      verificationMessage.value = response.data.message; // Assuming your backend sends a message
      setTimeout(() => {
          router.push('/login');
      }, 1000);
      
  
    } catch (err) {
      if (err.response) {
        error.value = err.response.data.message || 'Verification failed.';
      } else {
        error.value = 'Network error or backend is unavailable.';
      }
    } finally {
      loading.value = false;
    }
  });
  </script>