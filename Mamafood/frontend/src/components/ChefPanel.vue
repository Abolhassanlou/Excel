<template>
  <div class="d-flex vh-100">
    <div class="sidebar bg-dark text-light p-3 d-flex flex-column">
      <div class="text-center mb-3">
        <img src="https://via.placeholder.com/80" class="rounded-circle mb-2" alt="Chef">
        <h5 class="mt-2">Chef John Doe</h5>
      </div>

      <ul class="nav flex-column mb-auto">
        <li class="nav-item">
          <router-link class="nav-link text-light d-flex align-items-center" to="/chef/profile">
            <i class="fas fa-user-circle me-2"></i> <span>Mein Profil</span>
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link text-light d-flex align-items-center" to="/chef/chefinfo">
            <i class="fas fa-info-circle me-2"></i> <span>Chef-Informationen</span>
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link text-light d-flex align-items-center" to="/chef/mydishes">
            <i class="fas fa-utensils me-2"></i> <span>Mein Essen</span>
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link text-light d-flex align-items-center" to="/chef/food-management">
            <i class="fas fa-cogs me-2"></i> <span>Essensverwaltung</span>
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link text-light d-flex align-items-center" to="/reset-password">
            <i class="fas fa-key me-2"></i> <span>Passwort zurücksetzen</span>
          </router-link>
        </li>
      </ul>

      <div class="mt-auto">
        <router-link class="nav-link text-light d-flex align-items-center btn btn-secondary mb-2" to="/home">
          <i class="fas fa-home me-2"></i> <span>Home</span>
        </router-link>
        <button class="nav-link text-light d-flex align-items-center btn btn-danger logout-btn" @click="logout">
          <i class="fas fa-sign-out-alt me-2"></i> <span>Abmelden</span>
        </button>
      </div>
    </div>

    <div class="content p-4 flex-grow-1">
      <RouterView></RouterView>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';

export default {
  name: "ChefPanel",
  setup() {
    const router = useRouter();

    const logout = () => {
      // Clear tokens from localStorage
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('expires_in');
      localStorage.removeItem('user_role');

      // Redirect to login page
      router.push('/login');
    };

    return {
      logout,
    };
  },
};
</script>

<style scoped>
.sidebar {
  width: 250px;
  background-color: #333;
  padding: 20px;
  position: fixed;
  height: 100%;
  top: 0;
  left: 0;
  bottom: 0;
}

.content {
  margin-left: 250px;
  padding: 20px;
  overflow-y: auto;
  height: 100vh;
}

.sidebar a {
  color: white;
  text-decoration: none;
}

.sidebar .nav-link:hover:not(.logout-btn) {
  color: #fd7e14 !important;
}
</style>
