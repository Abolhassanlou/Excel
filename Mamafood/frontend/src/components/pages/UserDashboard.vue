<template>
  <div class="dashboard">
    <header class="navbar">
    </header>

    <aside class="sidebar">
      <div v-if="user">
        <h3>Welcome {{ user.name }}</h3>

        <ul>
          <li>
            <button @click="showUserInfo" :class="{active: isUserInfoVisible}" class="sidebar-btn">
              BenutzerInformation
            </button>
          </li>
          <li>
            <button @click="openResetPassword" :class="{active:isResetPasswordModalOpen}" class="sidebar-btn">
              Passwort zurücksetzen
            </button>
          </li>
          <li>
            <button  class="sidebar-btn">
              My Orders
            </button>
          </li>
        </ul>
        <button v-if="isLoggedIn" @click="logout" class="logout-btn">Logout</button>
      
      </div>
    </aside>

    <div class="content">
      <div v-if="isUserInfoVisible" class="user-info-section">
          <h3> BenutzerInformation</h3>
          <p><strong>Name: </strong>{{ user?.name }}</p>
          <p><strong>Email: </strong>{{ user?.email }}</p>
        </div>
      <div v-if="isResetPasswordModalOpen" class="reset-password-section">
        <h3>Passwort zurücksetzen</h3>
        <input
          v-model="resetEmail"
          type="email"
          placeholder="Enter your email"
        />
        
        
        <button @click="sendResetPasswordEmail">Senden</button>
        <p v-if="resetMessage" class="reset-message">{{ resetMessage }}</p>
        <button @click="closeResetPassword" class="close-reset-btn">
          Schließen
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/utils/axios'; // Make sure this path is correct for your project
import { useRouter } from 'vue-router';
import { isLoggedIn } from '@/stores/auth'; // Import the shared isLoggedIn ref
import { setUser , clearUser } from '../../stores/auth';

const user = ref(null);
const error = ref(null);
const router = useRouter();

// State for Reset Password
const isResetPasswordModalOpen = ref(false);
const resetEmail = ref('');
const resetMessage = ref('');
const isUserInfoVisible = ref (false);


onMounted(async () => {
  try {
    const response = await api.get('/users/me');
    user.value = response.data; // Store the user data in `user.value`
    setUser(response.data);
  } catch (err) {
    console.error('Failed to fetch user data:', err);
    error.value = 'Failed to fetch user data. Please try again later.';
    clearUser();
    
    router.push('/login');
  }
});

const showUserInfo=() => {
  isUserInfoVisible.value = !isUserInfoVisible.value;
  if(isUserInfoVisible) {
  isResetPasswordModalOpen.value =false;
  }
  
}

const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('expires_in');
  clearUser();// Update the shared state to false on logout
  router.push('/login');
};

const openResetPassword = () => {
  isResetPasswordModalOpen.value = !isResetPasswordModalOpen.value;
  if(isResetPasswordModalOpen.value) {
    isUserInfoVisible.value = false;
    resetEmail.value = user.value?.email || '';
  } else {
    resetEmail.value='';
    resetMessage.value='';
  }
  
  
};

const closeResetPassword = () => {
  isResetPasswordModalOpen.value = false;
  resetEmail.value = '';
  resetMessage.value = '';
};

const sendResetPasswordEmail = async () => {
  try {
    const response = await api.post('/auth/forgot-password', {
      email: resetEmail.value,
    });
    resetMessage.value = 'Überprüfen Sie Ihre E-Mails, um Ihr Passwort zurückzusetzen.';
  } catch (err) {
    console.error('Error sending reset email:', err);
    resetMessage.value = 'Fehler beim Senden der E-Mail. Bitte versuche es später noch einmal.';
  }
};
</script>

<style scoped>
/* Your existing CSS styles remain the same */
.navbar {
  position: fixed;
  top: 0;
  width: 100%;
  background-color: #333; /* Example, change to your navbar color */
  z-index: 10; /* Make sure navbar is above the sidebar */
  padding: 10px;
  color: white;
  font-size: 18px;
}

/* Sidebar Styles */
.dashboard {
  display: flex; /* Use flexbox for layout */
  min-height: 100vh; /* Ensure dashboard takes full viewport height */
}

.sidebar {
  width: 250px;
  background-color: #000; /* Set to pure black */
  padding: 20px;
  position: fixed; /* Sidebar fixed on the side */
  top: 0; /* Align to top */
  left: 0;
  bottom: 0;
  color: white; /* Set text color to white */
  font-family: Arial, sans-serif; /* Set a clear font family */
  font-size: 16px; /* Set font size for readability */
  z-index: 9; /* Ensure sidebar is below the navbar if a separate navbar is used */
  padding-top: 70px; /* Adjust if your actual navbar height is more than 50px */
}

/* Content Area */
.content {
  margin-left: 250px; /* Sidebar width */
  flex-grow: 1; /* Allow content to take remaining space */
  padding: 20px;
  overflow-y: auto; /* Enable scrolling in the content area */
  padding-top: 70px; /* Adjust this based on the height of the navbar */
}
.sidebar-btn {
  background: none;
  border: none;
  padding: 8px;
  color :white;
  cursor: pointer;
  width: 100%;
  text-align: left;
}
.sidebar-btn.active,
.sidebar-btn:hover {
  background-color: #fd7e14;
}
.sidebar h2,
.sidebar h3 {
  color: white; /* Ensure header text is also white */
  margin: 0;
  padding-bottom: 10px;
}

.sidebar p {
  color: white; /* Ensure paragraph text is white */
  margin-bottom: 30px; /* Added more space below the email */
}

.sidebar ul {
  list-style: none; /* Remove bullet points */
  padding: 0; /* Remove default padding */
  margin-top: 20px; /* Add some space before the list */
}

.sidebar li {
  cursor: pointer;
  padding: 8px; /* Add padding for better click area */
  margin-bottom: 10px; /* Space between list items */
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.sidebar li:hover {
  background-color: #fd7e14; /* Highlight with orange on hover */
  color: white;
}

.sidebar li.active {
  background-color: #fd7e14; /* Highlight with orange when active */
  color: white;
}

.sidebar .logout-btn {
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 10px 20px;
  margin-top: 20px;
  cursor: pointer;
  border-radius: 4px;
  width: 100%; /* Make button full width of sidebar */
  text-align: center;
}

.logout-btn:hover {
  background-color: #e02a2a;
}

.sidebar a {
  color: white; /* Set links color to white */
  text-decoration: none;
  display: block;
  margin-bottom: 10px; /* Add space between links */
  padding: 8px;
  border-radius: 4px;
}

.sidebar a:hover {
  background-color: #fd7e14; /* Highlight link on hover with orange */
  color: white; /* Keep text color white on hover */
}

.sidebar ul {
  display: flex;
  flex-direction: column;
  
}
.side button{
  width: 100%;
  text-align: left;
  
  box-sizing: border-box;
}

/* The .sidebar .nav-link:hover:not(.logout-btn) is redundant if all `a` tags are styled */
/* .sidebar .nav-link:hover:not(.logout-btn) {
  color: #fd7e14 !important;
} */

/* Reset Password Section Styles */
.reset-password-section {
  margin-top: 20px;
  padding: 15px;
  border-top: 1px solid #eee; /* Light gray line for separation */
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.reset-password-section h3 {
  font-size: 18px;
  margin-bottom: 10px;
  color: #333;
}

.reset-password-section input {
  width: calc(100% - 20px); /* Adjust for padding */
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
  box-sizing: border-box; /* Include padding in width */
}

.reset-password-section button {
  background-color: #fd7e14;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
  transition: background-color 0.3s ease;
}

.reset-password-section button:hover {
  background-color: #e66b0a; /* Slightly darker orange on hover */
}

.reset-message {
  color: #28a745; /* Green color for success messages */
  margin-top: 10px;
  font-weight: bold;
}

.close-reset-btn {
  background-color: #6c757d; /* Grey color for close button */
}

.close-reset-btn:hover {
  background-color: #545b62;
}

/* Add some padding-right to the content for smaller screens if sidebar is fixed */
@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    position: relative;
    top: auto;
    padding-top: 20px;
  }
  .content {
    margin-left: 0; /* Remove margin when sidebar is hidden */
    padding-top: 20px; /* Adjust content top padding for small screens */
  }
  .dashboard {
    flex-direction: column; /* Stack elements vertically on small screens */
  }
}
</style>
