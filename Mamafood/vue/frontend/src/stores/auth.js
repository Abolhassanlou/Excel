import { defineStore } from 'pinia';
import axios from 'axios';

// Set the base URL for your API
axios.defaults.baseURL = 'http://localhost:8000';  // Use the correct API base URL

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: null
  }),
  
  actions: {
    // Login method to authenticate the user and fetch the token
    async login(email, password) {
      try {
        // Create a new URLSearchParams object with the form data
        const formData = new URLSearchParams();
        formData.append('username', email);  // Use 'username' for the email
        formData.append('password', password);
    
        // Send the request with the correct headers and data format
        const response = await axios.post('http://localhost:8000/login', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',  // Set the correct content type
          },
        });
    
        this.token = response.data.access_token;
        localStorage.setItem('token', this.token); // Persist token
        await this.fetchUserData();  // Fetch user data after login
      } catch (error) {
        console.error('Login failed:', error.response?.data?.detail || error.message);
        throw new Error('Invalid email or password');
      }
    },

    // Fetch user data from the protected route
    async fetchUserData() {
      try {
        const response = await axios.get('http://localhost:8000/protected', {
          headers: { Authorization: `Bearer ${this.token}` },
        });
        this.user = response.data.user;  // Store user data
      } catch (error) {
        console.error('Failed to fetch user data:', error);
      }
    },

    // Signup method to register a new user
    async signup(username, email, password) {
      try {
        const response = await axios.post('http://localhost:8000/signup', { username, email, password });
        this.user = response.data;
        return true;
      } catch (error) {
        console.error('Signup error:', error);
        return false;
      }
    },
   

    // Logout method to clear user data and token
    logout() {
      this.token = '';
      this.user = null;
      localStorage.removeItem('token');
      window.location.href = '/login'; // Redirect to login page after logout
    },
  },

  persist: true,  // Automatically persist Pinia store in localStorage
});
