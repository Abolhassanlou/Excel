<template>
  <nav class="navbar">
    <RouterLink to="/" class="logo">Mama Food</RouterLink>
    <div class="hamburger" @click="toggleMenu">
      &#9776;
    </div>
    <div class="links" :class="{ open: isMenuOpen }">
      <RouterLink v-if="!isLoggedIn" to="/login" class="nav-item">Login</RouterLink>
      <RouterLink v-if="!isLoggedIn" to="/signup" class="nav-item">Registrieren</RouterLink>
      <RouterLink v-if="isLoggedIn" :to="homeOrDashboardLink" class="nav-item">
        {{ homeOrDashboardText }}
      </RouterLink>
      <RouterLink v-if="!isLoggedIn " to="/chefinfo" class="nav-item">Sei Chef</RouterLink>
      <button v-if="isLoggedIn" @click="handleLogout" class="nav-item logout-btn">Logout</button>
    </div>
  </nav>
</template>
<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { isLoggedIn, user, clearUser } from '@/stores/auth'; // Import shared state and functions
const isMenuOpen = ref(false);
const router = useRouter();

// Determines the text for the dynamic dashboard link
const homeOrDashboardText = computed(() => {
  const role = user.value?.role; // Access the role from the reactive user store
  if (isLoggedIn.value) { // Only show dashboard text if logged in
    if (role === 1) { // Chef
      return 'Chef-Dashboard';
    } else if (role === 0) { // Regular user
      return 'User-Dashboard';
    }
  }
  return 'Home'; // Default for non-logged-in or unassigned roles
});
// Determines the link destination for the dynamic dashboard link
const homeOrDashboardLink = computed(() => {
  const role = user.value?.role; // Access the role from the reactive user store
  if (isLoggedIn.value) { // Only provide dashboard links if logged in
    switch (role) {
      case 0: // Role 0 for regular user/customer
        return '/userdashboard';
      case 1: // Role 1 for chef
        return '/chefdashboard'; // Assuming this is the chef's specific dashboard path
      default:
        return '/'; // Fallback for other logged-in roles or undefined
    }
  }
  return '/'; // Default to home for guests
});
const handleLogout = () => {
  // `clearUser` from '@/stores/auth' already handles removing items from localStorage
  // and resetting isLoggedIn/user state.
  clearUser();
  // Redirect to the login page
  router.push('/login');
};
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};
</script>
<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 30px;
  background-color: #fff;
  color: #333;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  border-bottom: 2px solid #f0f0f0;
  position: sticky;
  top: 0;
  z-index: 1000;
}
/* Logo always shown */
.logo {
  font-size: 26px;
  font-weight: bold;
  color: #34495e;
  text-decoration: none;
}
/* Hamburger icon */
.hamburger {
  display: none;
  font-size: 26px;
  cursor: pointer;
}
/* Navigation links */
.links {
  display: flex;
  gap: 20px;
  align-items: center;
}
.nav-item {
  font-size: 16px;
  color: #f39c12;
  text-decoration: none;
  padding: 10px 15px;
  border-radius: 5px;
  transition: all 0.3s ease;
  cursor: pointer;
}
.nav-item:hover {
  background-color: #ffba58;
  color: white;
}
.logout-btn {
  background-color: #e74c3c;
  color: white;
  border: none;
}
.logout-btn:hover {
  background-color: #c0392b;
}
/* Responsive */
@media (max-width: 768px) {
  .hamburger {
    display: block;
  }
  .links {
    display: none;
    flex-direction: column;
    width: 100%;
    margin-top: 10px;
  }
  .links.open {
    display: flex;
  }
  .nav-item {
    width: 100%;
    text-align: center;
  }
}
</style> 