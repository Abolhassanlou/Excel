<template>
    <div>
      <h1>Become a Chef</h1>
      <form @submit.prevent="signup">
        <input type="text" v-model="chefData.name" placeholder="Name" />
        <input type="text" v-model="chefData.experience" placeholder="Experience" />
        <button type="submit">Signup</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  const chefData = ref({
    name: '',
    experience: '',
  });
  const router = useRouter();
  
  async function signup() {
    const token = localStorage.getItem('token');
    try {
      await axios.post('http://127.0.0.1:8000/chef-signup', chefData.value, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      router.push('/dashboard');
    } catch (error) {
      console.error('Error chef signup:', error);
    }
  }
  </script>