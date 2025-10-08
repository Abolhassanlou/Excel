<template>
  <div class="restaurant-registration-container">
    <h2>Restaurant Registration</h2>
    <form @submit.prevent="submitRegistration" class="registration-form">
      <section class="form-section">
        <h3>Your Account Information</h3>
        <div class="form-group">
          <label for="userName">Full Name:</label>
          <input type="text" id="userName" v-model="formData.user.name" required />
        </div>
        <div class="form-group">
          <label for="userEmail">Email:</label>
          <input type="email" id="userEmail" v-model="formData.user.email" required />
        </div>
        <div class="form-group">
          <label for="userPassword">Password:</label>
          <input type="password" id="userPassword" v-model="formData.user.password" required />
        </div>
      </section>
      <section class="form-section">
        <h3>Restaurant Details</h3>
        <div class="form-group">
          <label for="restaurantName">Restaurant Name:</label>
          <input type="text" id="restaurantName" v-model="formData.restaurant.restaurant_name" required />
        </div>
        <div class="form-group">
          <label for="telNumber">Telephone Number:</label>
          <input type="tel" id="telNumber" v-model="formData.restaurant.tel_number" required />
        </div>
        <div class="form-group">
          <label for="description">Description:</label>
          <textarea id="description" v-model="formData.restaurant.description" rows="5" required></textarea>
        </div>
        <div class="form-group">
          <label for="cuisine">Cuisine Type:</label>
          <select id="cuisine" v-model="formData.restaurant.cuisine_id" required>
            <option value="" disabled>Select a cuisine</option>
            <option v-for="cuisine in cuisines" :key="cuisine.id" :value="cuisine.id">
              {{ cuisine.cuisine_name }}
            </option>
          </select>

          <p v-if="loadingCuisines" class="info-message">Loading cuisines...</p>
          <p v-if="cuisineErrorMessage" class="error-message">{{ cuisineErrorMessage }}</p>
        </div>
        <div class="form-group">
          <label for="pickupTime">Typical Pickup Time:</label>
          <input type="time" id="pickupTime" v-model="formData.restaurant.pickup_time" required />
        </div>
          
      </section>
      <section class="form-section">
        <h3>Restaurant Address</h3>
        <div class="form-group">
          <label for="addressStreet">Street:</label>
          <input type="text" id="addressStreet" v-model="formData.address.street" required />
        </div>
        <div class="form-group">
          <label for="addressCity">City:</label>
          <input type="text" id="addressCity" v-model="formData.address.city" required />
        </div>
        <div class="form-group">
          <label for="addressPostalCode">Postal Code:</label>
          <input type="text" id="addressPostalCode" v-model="formData.address.postal_code" required />
        </div>
        <div class="form-group">
          <label for="addressFlatNumber">Flat Number:</label>
          <input type="text" id="addressFlatNumber" v-model="formData.address.flat_number" />
        </div>
        <div class="form-group">
          <label for="addressDoorNumber">Door Number:</label>
          <input type="text" id="addressDoorNumber" v-model="formData.address.door_number" />
        </div>
        <div class="form-group">
          <label for="googleMapsLink">Google Maps Link:</label>
          <input type="url" id="googleMapsLink" v-model="formData.address.google_maps_link" />
        </div>
        <div v-if="formSubmitted" class="thank-you-message">
          <p>Thank you for your registration. Please check your email to activate your account.</p>
        </div>
      </section>
      <button type="submit" :disabled="loading">
        {{ loading ? 'Registering...' : 'Register Restaurant' }}
      </button>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';

export default {
  name: 'ChefInfo',
  setup() {
    const formData = reactive({
      user: {
        name: '',
        email: '',
        password: '',
      },

      address: {
        street: '',
        city: '',
        postal_code: '',
        flat_number: '',
        door_number: '',
        google_maps_link: '', // Renamed and used consistently
      },

      restaurant: {
        restaurant_name: '',
        tel_number: '',
        description: '',
        cuisine_id: '',
        pickup_time: '12:00',
        image_url: '',
        
        
      },
    });
const cuisines = ref([]);
const loadingCuisines = ref(false);
const cuisineErrorMessage = ref('');
const loading = ref(false);
const errorMessage = ref('');
const formSubmitted = ref(false);
const API_BASE_URL = 'http://127.0.0.1:8000';

const fetchCuisines = async () => {
  loadingCuisines.value = true;
  cuisineErrorMessage.value = '';
  try {
    const response = await axios.get(`${API_BASE_URL}/cuisine/all/`);
    cuisines.value = response.data;
  } catch (error) {
    console.error('Error fetching cuisines:', error);
    cuisineErrorMessage.value = 'Failed to load cuisine options.';
    errorMessage.value = 'Failed to load cuisine options.';
  } finally {
    loadingCuisines.value = false;
  }
};

const submitRegistration = async () => {
  loading.value = true;
  errorMessage.value = '';
  try {
    formData.restaurant.cuisine_id = parseInt(formData.restaurant.cuisine_id);
    const response = await axios.post(`${API_BASE_URL}/restaurant/register-restaurant`, formData);
    if (response.status === 201) {
      alert("Registration successful! Please check your email.");
      formSubmitted.value = true;
      resetForm();
    }
  } catch (error) {
    console.error('Registration error:', error);
    errorMessage.value = error.response?.data?.detail || 'An unexpected error occurred during registration.';
  } finally {
    loading.value = false;
  }
};

const resetForm = () => {
  Object.assign(formData, {
    user: { name: '', email: '', password: '' },
    address: {
      street: '',
      city: '',
      postal_code: '',
      flat_number: '',
      door_number: '',
      google_maps_link: '',
    },
    restaurant: {
      restaurant_name: '',
      tel_number: '',
      description: '',
      cuisine_id: '',
      pickup_time: '12:00',
      
    },
  });
};

onMounted(() => {
  fetchCuisines();
});

return {
  formData,
  cuisines,
  loadingCuisines,
  cuisineErrorMessage,
  loading,
  errorMessage,
  submitRegistration,
  formSubmitted,
    };
  },

 };

</script>
<style scoped>
.restaurant-registration-container {
  max-width: 800px;
  margin: 50px auto;
  padding: 30px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
}
h2 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}
.form-section {
  background-color: #fff;
  padding: 20px;
  border-radius: 6px;
  margin-bottom: 25px;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);
}
.form-section h3 {
  color: #555;
  margin-top: 0;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}
.form-group {
  margin-bottom: 18px;
}
label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #444;
}
input,
textarea,
select {
  width: calc(100% - 20px);
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
  box-sizing: border-box;
}
textarea {
  resize: vertical;
}
button {
  display: block;
  width: 100%;
  padding: 15px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
button:hover:not(:disabled) {
  background-color: #45a049;
}
button:disabled {
  background-color: #a5d6a7;
  cursor: not-allowed;
}
.error-message {
  color: red;
  margin-top: 10px;
}
.info-message {
  color: #888;
  font-size: 14px;
}
.thank-you-message {
  background-color: #e0f7fa;
  border: 1px solid #4dd0e1;
  color: #00796b;
  padding: 15px;
  border-radius: 5px;
  margin-top: 15px;
}
</style>

