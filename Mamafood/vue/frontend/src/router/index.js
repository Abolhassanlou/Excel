// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Signup from '../views/Signup.vue';
import Protected from '../views/Protected.vue';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup,
  },
  {
    path:'/protected',
    name: 'Protected',
    component: Protected,
  }
  // You can add more routes here as needed
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
