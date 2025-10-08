// src/stores/auth.js
import { ref } from 'vue';

export const isLoggedIn = ref(false);
export const user = ref(null);

// Set user and login status
export const setUser = (userData) => {
  user.value = userData;
  isLoggedIn.value = true;

  try {
    localStorage.setItem('user_data', JSON.stringify(userData));
    localStorage.setItem('user_role', userData.role);
  } catch (e) {
    console.error("Error storing user data:", e);
  }
};

export const getRole = () => {
  return user.value?.role ?? parseInt(localStorage.getItem('user_role'), 10) ?? 0;
};

// Clear all auth-related data
export const clearUser = () => {
  user.value = null;
  isLoggedIn.value = false;
  localStorage.removeItem('user_data');
  localStorage.removeItem('user_role');
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('expires_in');
};

// Initialize from localStorage
const initializeAuth = () => {
  const token = localStorage.getItem('access_token');
  if (!token) return clearUser();

  isLoggedIn.value = true;

  try {
    const storedUser = JSON.parse(localStorage.getItem('user_data'));
    user.value = storedUser || { role: parseInt(localStorage.getItem('user_role'), 10) || 0 };
  } catch {
    user.value = { role: parseInt(localStorage.getItem('user_role'), 10) || 0 };
  }
};

// Run on import
initializeAuth();

// Sync if storage changes (e.g., in another tab)
window.addEventListener('storage', (event) => {
  if (['access_token', 'user_data', 'user_role'].includes(event.key)) {
    initializeAuth();
  }
});
