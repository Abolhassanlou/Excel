<template>
  <nav class="navbar">
    <!-- Logo always visible -->
    <RouterLink to="/" class="logo">Mama Food</RouterLink>

    <!-- Hamburger (mobile only) -->
    <div class="hamburger" @click="toggleMenu">
      &#9776;
    </div>

    <!-- Navigation Links (hidden on mobile until toggled) -->
    <div class="links" :class="{ open: isMenuOpen }">
      <!-- Login and Register only visible when NOT logged in -->
      <RouterLink v-if="!isLoggedIn" to="/login" class="nav-item">Login</RouterLink>
      <RouterLink v-if="!isLoggedIn" to="/signup" class="nav-item">Registrieren</RouterLink>

      <!-- Dynamic Home/Dashboard and Logout only visible when logged in -->
      <RouterLink v-if="isLoggedIn" :to="homeOrDashboardLink" class="nav-item">
        {{ homeOrDashboardText }}
      </RouterLink>
      <RouterLink to="/chef" class="nav-item">Sei Chef</RouterLink>
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

const homeOrDashboardText = computed(() => {
  const role = parseInt(localStorage.getItem('user_role'), 10);

  if (!isNaN(role)) {
     if (role === 1) return 'Chef-Dashboard';
     if (role === 0) return 'User-Dashb';
  }
  return 'Fedoghan';
});

// Computed property for the link destination of the home/dashboard link

const homeOrDashboardLink = computed(() => {
  // Ensure user object and role exist before checking
  const role = parseInt(localStorage.getItem('user_role'), 10);

    switch (role) {
      case 0: // Role 0 for regular user/customer
        return '/userdashboard';
      case 1: // Role 1 for chef
        return '/chef'; // Assuming this is the chef's specific dashboard path   
    }
  });


const handleLogout = () => {
  // Clear authentication tokens from localStorage
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('expires_in');

  // Update the shared authentication state
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
