<template>
  <div class="dashboard container-fluid">
    <div class="row">
      <aside class="col-md-3 col-lg-2 d-md-block bg-dark sidebar">
        <div class="position-sticky pt-3">
          <div v-if="user" class="text-white">
            <h3 class="px-3">Welcome {{ user.name }}</h3>

            <ul class="nav flex-column">
              <h4>Rest. Image</h4>
          <div class="restaurant-image-container">
            <img v-if="restaurant" :src="`http://localhost:8000${restaurant.image_url}`" :alt="`${restaurant?.restaurant_name || 'Restaurant'} image`"  class="restaurant-display-image" /> 
                                
    
    
          </div>
              <li class="nav-item">
                <button @click="showUserInfo" :class="{ active: isUserInfoVisible }" class="nav-link btn btn-link text-white">
                  BenutzerInformation
                </button>
              </li>
              <li class="nav-item">
                <button @click="openResetPassword" :class="{ active: isResetPasswordModalOpen }" class="nav-link btn btn-link text-white">
                  Passwort ändern
                </button>
              </li>
              <li class="nav-item">
                  <button @click="toggleManageRestaurant" :class="{ active: isManageRestaurant }" class="nav-link btn btn-link text-white">
                    Restaurant Info
                  </button>
              </li>
              <li class="nav-item">
                <button @click="toggleAddFood" :class="{ active: isAddFood }" class="nav-link btn btn-link text-white">
                  Gericht hinzufügen
                </button>
              </li>
              <li class="nav-item">
                <button @click="toggleManageMenu" :class="{ active: isManageMenu || isModifyFood }" class="nav-link btn btn-link text-white">
                  Manage Menu
                </button>
              </li>
            </ul>
          </div>
        </div>
      </aside>

      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">

        <div class="content">
          <div v-if="isUserInfoVisible" class="card">
            <div class="card-header">
              <h3>BenutzerInformation</h3>
            </div>
            <div class="card-body">
              <p><strong>Name:</strong> {{ user?.name }}</p>
              <p><strong>Email:</strong> {{ user?.email }}</p>
            </div>
          </div>

          <div v-if="isResetPasswordModalOpen" class="card">
            <div class="card-header">
              <h3>Passwort ändern</h3>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <label for="resetEmail" class="form-label">E-Mail eingeben</label>
                <input v-model="resetEmail" type="email" class="form-control" id="resetEmail" placeholder="E-Mail eingeben" />
              </div>
              <button @click="sendResetPasswordEmail" class="btn btn-primary">Senden</button>
              <button @click="closeResetPassword" class="btn btn-secondary ms-2">Schließen</button>
              <p v-if="resetMessage" class="alert alert-info mt-3">{{ resetMessage }}</p>
            </div>
          </div>
          <div v-if="isManageRestaurant" class="card">
          <div class="card-header">
              <h3>To modify restaurant detail please contact support</h3>
              </div>
          <div class="card-body">
                    <div>
                        <ul class="list-group">
                            <section class="form-section" v-if="restaurant">
                        <div class="restaurant-image-section">
                              <h4>Restaurant Image</h4>
                                <div class="restaurant-image-container">
                                    <img v-if="restaurant" :src="`http://localhost:8000${restaurant.image_url}`" :alt="`${restaurant?.restaurant_name || 'Restaurant'} image`"
                                    class="restaurant-display-image" /> 
                                </div>

                              <div class="image-upload-controls">
                                <label for="imageUpload" class="btn btn-primary"> Choose New Image
                                    <input type="file" id="imageUpload" @change="handleImageFileChange" accept="image/*" style="display: none;">
                                </label>
                                <button @click="uploadRestaurantImage" :disabled="!selectedImageFile || uploadingImage" class="btn btn-success"> {{ uploadingImage ? 'Uploading...' : 'Upload Image' }}
                                </button>
                                <button v-if="restaurant?.image_url" @click="removeRestaurantImage" :disabled="uploadingImage" class="btn btn-danger"> Remove Image
                                </button>
                                <p v-if="imageUploadMessage" :class="imageUploadError ? 'text-danger' : 'text-success'"> {{ imageUploadMessage }}
                                </p>
                              </div>
                          </div>
                          <!-- <p>Nanme: <strong>{{restaurant.image_url}}</strong> </p> -->
                          <p><strong>Name:</strong> {{ restaurant.restaurant_name }}</p>
                          <p><strong>Telephone:</strong> {{ restaurant.tel_number }}</p>
                          <p><strong>Description:</strong> {{ restaurant.description }}</p>
                          <p><strong>Pickup Time:</strong> {{ restaurant.pickup_time }}</p>
                          <p><strong>Cuisine type:</strong> {{ restaurant.cuisine?.cuisine_name }}</p>
                          <h4>Address</h4>
                          <p><strong>Street:</strong> {{ restaurant.address?.street }}</p>
                          <p v-if="restaurant.address?.door_number"><strong>Door number:</strong> {{ restaurant.address.door_number }}</p>
                          <p v-if="restaurant.address?.flat_number"><strong>Flat number:</strong> {{ restaurant.address.flat_number }}</p>
                          <p><strong>Postal Code:</strong> {{ restaurant.address?.postal_code }}</p>
                          <p><strong>City:</strong> {{ restaurant.address?.city }}</p>
                          <a v-if="restaurant.address?.google_maps_link" :href="restaurant.address.google_maps_link" target="_blank">View on Map</a>
                      </section>
                  </ul>
              </div>
          </div>
      </div>
          <div v-if="isAddFood" class="card">
            <div class="card-header">
              <h3>Neues Gericht hinzufügen</h3>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <label for="foodName" class="form-label">Name des Gerichts</label>
                <input type="text" v-model="newFood.name" class="form-control" id="foodName" placeholder="Name des Gerichts" />
              </div>
              <div class="mb-3">
                <label for="foodDescription" class="form-label">Beschreibung</label>
                <input type="text" v-model="newFood.description" class="form-control" id="foodDescription" placeholder="Beschreibung" />
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="price" class="form-label">Price in Euro:</label>
                  <div class="input-group">
                    <span class="input-group-text">€</span>
                    <input type="number" step="0.01" v-model="newFood.price" class="form-control" id="price" placeholder="Preis" />
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <label for="lagerbestand" class="form-label">Verfügbar:</label>
                  <input type="number" v-model="newFood.initial_stock" class="form-control" id="lagerbestand" placeholder="Lagerbestand" />
                </div>
              </div>
              <label class="form-label">Zubereitungszeit</label>
              <div class="row">
                <div class="col-md-4 mb-3">
                  <div class="input-group">
                    <input type="number" v-model="prepHours" min="0" max="23" class="form-control" placeholder="Hours">
                    <span class="input-group-text">H</span>
                  </div>
                </div>
                <div class="col-md-4 mb-3">
                  <div class="input-group">
                    <input type="number" v-model="prepMinutes" min="0" max="59" class="form-control" placeholder="Minutes">
                    <span class="input-group-text">M</span>
                  </div>
                </div>
                <div class="col-md-4 mb-3">
                  <div class="input-group">
                    <input type="number" v-model="prepSeconds" min="0" max="59" class="form-control" placeholder="Seconds">
                    <span class="input-group-text">S</span>
                  </div>
                </div>
              </div>
              <div class="mb-3">
                <label for="imageUrl" class="form-label">Bild-URL (optional)</label>
                <input type="text" v-model="newFood.image_url" class="form-control" id="imageUrl" placeholder="Bild-URL (optional)" />
              </div>
              <div class="mb-3">
                <h5>Category: choose at least one</h5>
                <div class="d-flex flex-wrap gap-3">
                  <div v-for="cat in categories" :key="cat.id" class="form-check">
                    <input class="form-check-input" type="checkbox" :value="cat.id" :id="'cat-' + cat.id" v-model="newFood.categories" />
                    <label class="form-check-label" :for="'cat-' + cat.id">
                      {{ cat.name }}
                    </label>
                  </div>
                </div>
              </div>
              <button @click="submitFood" class="btn btn-success">Hinzufügen</button>
              <p v-if="foodMessage" class="alert alert-info mt-3">{{ foodMessage }}</p>
            </div>
          </div>

          <div v-if="isManageMenu" class="card">
         
            <div class ="card-header">
              <h3> Alle Gerichte</h3>
            </div>
            <div class ="card-body">
              <div v-if ="foodList.length===0">
                <p> Keine Gerichte gefunden.</p>
              </div>
              <div v-else>
                <ul class="list-group">
                  <li v-for="food in foodList" :key ="food.id" class="list-group-item">
                    <div class="d-flex flex-wrap align-items-start gap-4">
                      <div class=" p-3 border rounded bg-light">
                        <!-- Image Display -->
                        <div class=" text-center mb-3">
                          <img 
                            :src="`http://localhost:8000${food.image_url}`"
                            :alt="`${food?.name || 'Food'} image`"
                            class="img-thumbnail img-fluid rounded shadow"
                            style="max-width: 200px; max-height: 150px;"
                          />
                        </div>

                        <!-- Image Upload Buttons -->
                        <div class=" d-flex flex-wrap justify-content-center gap-2 mb-2">
                          <label class="btn btn-primary">
                            New Image
                            <input
                              type="file"
                              id="imageUpload-{{ food.id }}"
                              @change="handleFoodImageFileChange(food, $event)"
                              accept="image/*"
                              style="display: none;"
                            />
                          </label>

                          <button
                            @click="uploadFoodImage(food)"
                            :disabled="!food.selectedFile || food.uploading"
                            class="btn btn-success"
                          >
                            {{ food.uploading ? 'Uploading...' : 'Upload' }}
                          </button>

                          <button
                            v-if="food.image_url"
                            @click="removeFoodImage(food)"
                            :disabled="food.uploading"
                            class="btn btn-danger"
                          >
                            Remove
                          </button>
                        </div>

                        <!-- Upload Message -->
                        <p
                            v-if="food.uploadMessage"
                            :class="['text-center', food.uploadError ? 'text-danger' : 'text-success']"
                          >
                            {{ food.uploadMessage }}
                          </p>
                      </div>
                    <div>
                    <strong>Name: {{ food.name }}</strong> <br/>
                    <span>description: {{food.description}}</span> <br/>
                    <span>categories: {{ food.categories.map(c => c.name).join(' , ') }}</span> <br/>
                    <span>Preis: € {{ food.price }}</span> <br/>
                    <span>Lager: {{ food.initial_stock }}</span> <br/>
                    <span>Zubereitung : {{ food.preparation_time }}</span><br/>
                    
                    <button @click="modifyFood(food)" class="btn btn-primary">Modify</button>
                    <button @click="deleteFood(food)" class="btn btn-danger ms-2">Delete</button></div>
     
                    </div>
                    
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <div v-if="isModifyFood" class="card">
            <div class="card-header">
              <h3>Gericht bearbeiten: {{ currentEditingFood.name }}</h3>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <label for="editFoodName" class="form-label">Name des Gerichts</label>
                <input type="text" v-model="currentEditingFood.name" class="form-control" id="editFoodName" placeholder="Name des Gerichts" />
              </div>
              <div class="mb-3">
                <label for="editFoodDescription" class="form-label">Beschreibung</label>
                <input type="text" v-model="currentEditingFood.description" class="form-control" id="editFoodDescription" placeholder="Beschreibung" />
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="editPrice" class="form-label">Price in Euro:</label>
                  <div class="input-group">
                    <span class="input-group-text">€</span>
                    <input type="number" step="0.01" v-model="currentEditingFood.price" class="form-control" id="editPrice" placeholder="Preis" />
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <label for="editLagerbestand" class="form-label">Verfügbar:</label>
                  <input type="number" v-model="currentEditingFood.initial_stock" class="form-control" id="editLagerbestand" placeholder="Lagerbestand" />
                </div>
              </div>
              <label class="form-label">Zubereitungszeit</label>
              <div class="row">
                <div class="col-md-4 mb-3">
                  <div class="input-group">
                    <input type="number" v-model="editPrepHours" min="0" max="23" class="form-control" placeholder="Hours">
                    <span class="input-group-text">H</span>
                  </div>
                </div>
                <div class="col-md-4 mb-3">
                  <div class="input-group">
                    <input type="number" v-model="editPrepMinutes" min="0" max="59" class="form-control" placeholder="Minutes">
                    <span class="input-group-text">M</span>
                  </div>
                </div>
                <div class="col-md-4 mb-3">
                  <div class="input-group">
                    <input type="number" v-model="editPrepSeconds" min="0" max="59" class="form-control" placeholder="Seconds">
                    <span class="input-group-text">S</span>
                  </div>
                </div>
              </div>
              <div class="mb-3">
                <label for="editImageUrl" class="form-label">Bild-URL (optional)</label>
                <input type="text" v-model="currentEditingFood.image_url" class="form-control" id="editImageUrl" placeholder="Bild-URL (optional)" />
              </div>
              <div class="mb-3">
                <h5>Category: choose at least one</h5>
                <div class="d-flex flex-wrap gap-3">
                  <div v-for="cat in categories" :key="cat.id" class="form-check">
                    <input class="form-check-input" type="checkbox" :value="cat.id" :id="'edit-cat-' + cat.id" v-model="currentEditingFood.categories" />
                    <label class="form-check-label" :for="'edit-cat-' + cat.id">
                      {{ cat.name }}
                    </label>
                  </div>
                </div>
              </div>
              <button @click="saveModifiedFood" class="btn btn-success">Speichern</button>
              <button @click="cancelModifyFood" class="btn btn-secondary ms-2">Abbrechen</button>
              <p v-if="modifyFoodMessage" class="alert alert-info mt-3">{{ modifyFoodMessage }}</p>
            </div>
          </div>
        </div>
        
      </main>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, reactive } from 'vue';
import api from '@/utils/axios'; // Your Axios instance
import { useRouter } from 'vue-router';
import { isLoggedIn, setUser, clearUser } from '@/stores/auth';

const router = useRouter();
const user = ref(null);
const error = ref(null);

// Section visibility states
const isResetPasswordModalOpen = ref(false);
const isUserInfoVisible = ref(true); // Show user info by default
const isAddFood = ref(false);
const isManageMenu = ref(false);
const isModifyFood = ref(false); // State for modify food section
const isManageRestaurant = ref(false); // Controls visibility of restaurant info (image-only) section

// Reset password data
const resetEmail = ref('');
const resetMessage = ref('');

// Categories for food items (used by food management sections)
const categories = ref([]);

// Food related refs (used by Add Food and Manage Menu sections)
const prepHours = ref(0);
const prepMinutes = ref(20);
const prepSeconds = ref(0);
const newFood = ref({
  name: '',
  description: '',
  price: 6.5,
  initial_stock: 40,
  preparation_time: '',
  image_url: '', // Image URL for food items
  categories: [],
  restaurant_id: '',
});
const foodMessage = ref('');
const foodList = ref([]);
const foodLoadError = ref('');
const currentEditingFood = ref(null);
const modifyFoodMessage = ref('');
const editPrepHours = ref(0);
const editPrepMinutes = ref(0);
const editPrepSeconds = ref(0);

// **Restaurant data** (This `ref` will hold the full restaurant object fetched from API)
// It's crucial for displaying existing restaurant details and constructing payloads for image updates.
const restaurant = ref(null);
const resLoadError = ref(''); // Error message for restaurant data loading

// --- **NEW: Refs for Restaurant Image Upload/Removal** ---
const selectedImageFile = ref(null); // Holds the file object selected by the user
const uploadingImage = ref(false); // True when an image upload/removal is in progress
const imageUploadMessage = ref(''); // Feedback message to the user (e.g., "Uploading...", "Success!")
const imageUploadError = ref(false); // True if there's an error during image operation
const loading = ref(true); // General loading indicator for initial data fetch

// --- **Lifecycle Hook: onMounted** ---
onMounted(async () => {
  loading.value = true;
  try {
    const response = await api.get('/users/me');
    user.value = response.data;
    setUser(response.data);
  } catch (err) {
    error.value = 'Fehler beim Laden der Benutzerdaten.';
    clearUser();
    router.push('/login');
    return;
  }

  try {
    const responseCategories = await api.get('/category/all/');
    categories.value = responseCategories.data;
  } catch (err) {
    error.value = 'Fehler beim Laden der Kategorien.';
  }

  // Initial fetch of restaurant ID and data for the sidebar image display.
  // This ensures the image is shown as soon as the component loads, if applicable.
  try {
    if (user.value?.id) {
      const id = user.value.id;
      const resRestaurant = await api.get(`/restaurant/user_id/${id}`);
      const idr = resRestaurant.data.restaurant_id;

      if (idr) {
        newFood.value.restaurant_id = idr; // Set restaurant ID for new food items
        const restinfo = await api.get(`/restaurant/${idr}`);
        restaurant.value = restinfo.data; // Store full restaurant data
      } else {
        error.value = "Keine Restaurant-ID für diesen Benutzer gefunden.";
      }
    }
  } catch (err) {
    console.error('Fehler beim Laden der Restaurant-ID oder Daten:', err);
    error.value = 'Fehler beim Laden der Restaurant-Informationen.';
  } finally {
    loading.value = false;
  }
});

// Helper to pad numbers for time formatting (used by food items)
const pad = (num) => String(num).padStart(2, '0');

// --- **UI Section Toggles** ---
// Centralized function to hide all content sections
const hideAllContentSections = () => {
  isUserInfoVisible.value = false;
  isResetPasswordModalOpen.value = false;
  isAddFood.value = false;
  isManageMenu.value = false;
  isModifyFood.value = false;
  isManageRestaurant.value = false; // Hide the restaurant info/image section
};

const showUserInfo = () => {
  hideAllContentSections();
  isUserInfoVisible.value = true;
};

const openResetPassword = () => {
  hideAllContentSections();
  isResetPasswordModalOpen.value = true;
  resetEmail.value = user.value?.email || '';
};

const closeResetPassword = () => {
  isResetPasswordModalOpen.value = false;
  resetEmail.value = '';
  resetMessage.value = '';
};

// Toggle for Add Food section
const toggleAddFood = () => {
  hideAllContentSections();
  isAddFood.value = true;
  // Reset newFood form
  newFood.value = { name: '', description: '', price: 1.5, initial_stock: 40, preparation_time: '', image_url: '', categories: [], restaurant_id: newFood.value.restaurant_id };
  prepHours.value = 0;
  prepMinutes.value = 20;
  prepSeconds.value = 0;
  foodMessage.value = '';
};

// Toggle for Manage Menu section
const toggleManageMenu = async () => {
  hideAllContentSections();
  isManageMenu.value = true;
  foodLoadError.value = '';

  try {
    const id = user.value.id;
    const resRestaurant = await api.get(`/restaurant/user_id/${id}`);
    const idr = resRestaurant.data.restaurant_id;

    if (!idr) {
      throw new Error("Restaurant ID not found for this user");
    }

    const resFood = await api.get(`/food/food_restaurant_id/${idr}`);
    foodList.value = resFood.data.map(food => ({
      ...food,
      selectedFile: null, // Add a new reactive property for each food item
      uploading: false,
      uploadMessage: '',
      uploadError: false,
    }));
  } catch (err) {
    foodLoadError.value = 'Fehler beim Laden der Gerichte';
    console.error(err);
  }
};

// --- **RESTAURANT INFO (DISPLAY + IMAGE MODIFICATION) MANAGEMENT** ---
const toggleManageRestaurant = async () => {
  hideAllContentSections(); // Hide all other sections first
  isManageRestaurant.value = true; // Show the restaurant info section

  // Reset image-related state for a clean start whenever this section is opened
  selectedImageFile.value = null;
  imageUploadMessage.value = '';
  imageUploadError.value = false;
  resLoadError.value = ''; // Clear previous loading errors for this section

  try {
    const id = user.value.id;
    const resRestaurant = await api.get(`/restaurant/user_id/${id}`);
    const idr = resRestaurant.data.restaurant_id;

    if (!idr) {
      restaurant.value = null; // Clear any old restaurant data
      resLoadError.value = 'No restaurant found for this user. Restaurant info cannot be displayed or image managed.';
      return;
    }

    const restinfo = await api.get(`/restaurant/${idr}`);
    restaurant.value = restinfo.data; // Store the fetched data for display and for image operations

  } catch (err) {
    console.error('Error loading restaurant data:', err);
    resLoadError.value = err.response?.data?.detail || 'Failed to load restaurant information.';
    restaurant.value = null; // Clear data on error
  }
};
// --- **IMAGE UPLOAD/REMOVE FUNCTIONS Food (Using Dedicated API)** ---
// Function to handle file input change (when user selects a file)
    const handleFoodImageFileChange = (food, event) => {
      const file = event.target.files[0];
      if (file) {
        food.selectedFile = file;
        food.uploadMessage = `Selected: ${file.name}`;
        food.uploadError = false;
      } else {
        food.selectedFile = null;
        food.uploadMessage = '';
      }
    };

// This function makes the PATCH request to your backend's dedicated image update endpoint

const updateFoodImageUrlInDB = async (foodId , newImageUrl) => {
    try {
        // Assuming your dedicated API endpoint is PATCH /restaurant/{id}/image
        // and expects a JSON body like {"image_url": "new_url" or null}
        const response = await api.patch(`/food/${foodId}/image`, {
            image_url: newImageUrl,
        });

        if (response.status === 200) {
            console.log('Food image URL updated in DB successfully via dedicated API.');
        } else {
            // If the API returns a non-200 status but not an error (e.g., 204 No Content), handle it.
            // Otherwise, throw an error to be caught.
            throw new Error(`Dedicated image update API returned status: ${response.status}`);
        }
    } catch (error) {
        console.error('Failed to update Food image URL via dedicated API:', error);
        // Rethrow the error so the calling function can display a user-friendly message
        throw error;
    }
};

// This function handles the full process of uploading a new image file
const uploadFoodImage = async (food) => {
  if (!food.selectedFile) {
    food.uploadMessage = 'Please select an image file first.';
    food.uploadError = true;
    return;
  }

  food.uploading = true;
  food.uploadMessage = 'Uploading file...';
  food.uploadError = false;

  const formDataForFile = new FormData();
  formDataForFile.append('image', food.selectedFile);

  try {
    const uploadResponse = await api.post(`/food/upload&food/image/`, formDataForFile, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    if (uploadResponse.status === 200 && uploadResponse.data.image_url) {
      const newImageUrl = uploadResponse.data.image_url;
      await updateFoodImageUrlInDB(food.id, newImageUrl);

      // Update the local food item object for immediate UI display
      food.image_url = newImageUrl;
      food.uploadMessage = 'Image uploaded and saved successfully!';
      food.uploadError = false;
      food.selectedFile = null; // Clear the file input
    } else {
      throw new Error('File upload failed or no image URL received from server.');
    }
  } catch (error) {
    console.error('Image upload process error:', error);
    food.uploadMessage = error.response?.data?.detail || 'Failed to upload or update image. Please try again.';
    food.uploadError = true;
  } finally {
    food.uploading = false;
  }
};

// This function handles removing the current image
const removeFoodImage = async (food) => {
    if (!confirm('Are you sure you want to remove the current food image?')) {
        return;
    }
    if (!food.id) {
        food.uploadMessage = 'Food data not loaded. Cannot remove image.';
        food.uploadError = true;
        return;
    }

    food.uploading = true;
    food.uploadMessage = 'Removing image...';
    food.uploadError = false;

    try {
        // Step 1: Update the restaurant's image_url in the database to null using the DEDICATED API
        await updateFoodImageUrlInDB(food.id, null);

        // Step 2: Update the local `restaurant.value` ref for immediate UI display
        food.image_url = null;
        food.uploadMessage = 'Food image removed successfully!';
        food.uploadError = false;
        food.selectedFile = null; // Clear any file previously selected

    } catch (error) {
        console.error('Error removing image:', error);
        food.uploadMessage = error.response?.data?.detail || 'Error removing image. Please try again.';
        food.uploadError = true;
    } finally {
    food.uploading = false;
    }
};

// --- **IMAGE UPLOAD/REMOVE FUNCTIONS Restuarant (Using Dedicated API)** ---

// Function to handle file input change (when user selects a file)
const handleImageFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
        selectedImageFile.value = file;
        imageUploadMessage.value = `Selected: ${file.name}`;
        imageUploadError.value = false;
    } else {
        selectedImageFile.value = null;
        imageUploadMessage.value = '';
    }
};

// This function makes the PATCH request to your backend's dedicated image update endpoint
// It's a helper for uploadRestaurantImage and removeRestaurantImage
const updateRestaurantImageUrlInDB = async (restaurantId, newImageUrl) => {
    try {
        // Assuming your dedicated API endpoint is PATCH /restaurant/{id}/image
        // and expects a JSON body like {"image_url": "new_url" or null}
        const response = await api.patch(`/restaurant/${restaurantId}/image`, {
            image_url: newImageUrl,
        });

        if (response.status === 200) {
            console.log('Restaurant image URL updated in DB successfully via dedicated API.');
        } else {
            // If the API returns a non-200 status but not an error (e.g., 204 No Content), handle it.
            // Otherwise, throw an error to be caught.
            throw new Error(`Dedicated image update API returned status: ${response.status}`);
        }
    } catch (error) {
        console.error('Failed to update restaurant image URL via dedicated API:', error);
        // Rethrow the error so the calling function can display a user-friendly message
        throw error;
    }
};

// This function handles the full process of uploading a new image file
const uploadRestaurantImage = async () => {
    // Frontend validation
    if (!selectedImageFile.value) {
        imageUploadMessage.value = 'Please select an image file first.';
        imageUploadError.value = true;
        return;
    }
    if (!restaurant.value || !restaurant.value.id) {
        imageUploadMessage.value = 'Restaurant data not loaded. Cannot upload image.';
        imageUploadError.value = true;
        return;
    }

    uploadingImage.value = true; // Set loading state
    imageUploadMessage.value = 'Uploading file...';
    imageUploadError.value = false;

    // Prepare FormData for file upload
    const formDataForFile = new FormData();
    formDataForFile.append('image', selectedImageFile.value); // 'image' matches your FastAPI @Restaurant_router.post("/upload&restaurant/image/") parameter name

    try {
        // Step 1: Upload the image file to your dedicated file upload endpoint
        const uploadResponse = await api.post(`/restaurant/upload&restaurant/image/`, formDataForFile, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });

        if (uploadResponse.status === 200 && uploadResponse.data.image_url) {
            const newImageUrl = uploadResponse.data.image_url;

            // Step 2: Update the restaurant's image_url in the database using the DEDICATED API
            await updateRestaurantImageUrlInDB(restaurant.value.id, newImageUrl);

            // Step 3: Update the local `restaurant.value` ref for immediate UI display
            restaurant.value.image_url = newImageUrl;

            imageUploadMessage.value = 'Image uploaded and saved successfully!';
            imageUploadError.value = false;
            selectedImageFile.value = null; // Clear the file input
        } else {
            throw new Error('File upload failed or no image URL received from server.');
        }
    } catch (error) {
        console.error('Image upload process error:', error);
        imageUploadMessage.value = error.response?.data?.detail || 'Failed to upload or update image. Please try again.';
        imageUploadError.value = true;
    } finally {
        uploadingImage.value = false; // Reset loading state
    }
};

// This function handles removing the current image
const removeRestaurantImage = async () => {
    if (!confirm('Are you sure you want to remove the current restaurant image?')) {
        return;
    }
    if (!restaurant.value || !restaurant.value.id) {
        imageUploadMessage.value = 'Restaurant data not loaded. Cannot remove image.';
        imageUploadError.value = true;
        return;
    }

    uploadingImage.value = true; // Set loading state
    imageUploadMessage.value = 'Removing image...';
    imageUploadError.value = false;

    try {
        // Step 1: Update the restaurant's image_url in the database to null using the DEDICATED API
        await updateRestaurantImageUrlInDB(restaurant.value.id, null);

        // Step 2: Update the local `restaurant.value` ref for immediate UI display
        restaurant.value.image_url = null;

        imageUploadMessage.value = 'Restaurant image removed successfully!';
        imageUploadError.value = false;
        selectedImageFile.value = null; // Clear any file previously selected

    } catch (error) {
        console.error('Error removing image:', error);
        imageUploadMessage.value = error.response?.data?.detail || 'Error removing image. Please try again.';
        imageUploadError.value = true;
    } finally {
        uploadingImage.value = false; // Reset loading state
    }
};


// Submit new food
const submitFood = async () => {
  newFood.value.preparation_time = `${pad(prepHours.value)}:${pad(prepMinutes.value)}:${pad(prepSeconds.value)}`;

  if (!newFood.value.name || !newFood.value.description || newFood.value.price <= 0 || !newFood.value.restaurant_id) {
    foodMessage.value = 'Bitte füllen Sie alle Felder korrekt aus.';
    return;
  }
  if (newFood.value.categories.length === 0) {
    foodMessage.value = 'Bitte wählen Sie mindestens eine Kategorie aus.';
    return;
  }

  try {
    await api.post('/food', newFood.value);
    foodMessage.value = 'Gericht erfolgreich hinzugefügt!';
    // Optionally refresh the manage menu list if it's visible
    if (isManageMenu.value) {
      await toggleManageMenu();
    }
    // Reset the form
    newFood.value = { name: '', description: '', price: 1.5, initial_stock: 40, image_url: '', categories: [], restaurant_id: newFood.value.restaurant_id };
    prepHours.value = 0;
    prepMinutes.value = 20;
    prepSeconds.value = 0;
  } catch (err) {
    console.error('Fehler beim Hinzufügen:', err);
    foodMessage.value = 'Fehler beim Hinzufügen. Bitte erneut versuchen.';
  }
};

// Send reset password email
const sendResetPasswordEmail = async () => {
  try {
    await api.post('/auth/forgot-password', { email: resetEmail.value });
    resetMessage.value = 'Überprüfen Sie Ihre E-Mail zum Zurücksetzen.';
  } catch (err) {
    console.error('Fehler beim Senden der E-Mail:', err);
    resetMessage.value = 'Fehler. Versuchen Sie es später erneut.';
  }
};

// Function to handle modifying a food item
const modifyFood = (food) => {
  isManageMenu.value = false; // Hide the food list
  isAddFood.value = false;
  isUserInfoVisible.value = false;
  isResetPasswordModalOpen.value = false;
  isModifyFood.value = true; // Show the modify food form

  // Deep copy the food object to prevent direct mutation of the list item
  currentEditingFood.value = JSON.parse(JSON.stringify(food));

  // Extract hours, minutes, seconds from preparation_time string
  const timeParts = currentEditingFood.value.preparation_time.split(':').map(Number);
  editPrepHours.value = timeParts[0] || 0;
  editPrepMinutes.value = timeParts[1] || 0;
  editPrepSeconds.value = timeParts[2] || 0;

  // Ensure categories are numerical IDs for the checkboxes
  if (currentEditingFood.value.categories && currentEditingFood.value.categories.length > 0) {
    currentEditingFood.value.categories = currentEditingFood.value.categories.map(cat => cat.id);
  } else {
    currentEditingFood.value.categories = [];
  }

  modifyFoodMessage.value = ''; // Clear any previous messages
};

// Function to save modified food item
const saveModifiedFood = async () => {
  if (!currentEditingFood.value) return;

  // Format preparation time back to HH:MM:SS
  currentEditingFood.value.preparation_time = `${pad(editPrepHours.value)}:${pad(editPrepMinutes.value)}:${pad(editPrepSeconds.value)}`;

  if (!currentEditingFood.value.name || !currentEditingFood.value.description || currentEditingFood.value.price <= 0) {
    modifyFoodMessage.value = 'Bitte füllen Sie alle Felder korrekt aus.';
    return;
  }
  if (currentEditingFood.value.categories.length === 0) {
    modifyFoodMessage.value = 'Bitte wählen Sie mindestens eine Kategorie aus.';
    return;
  }

  try {
    // Assuming your API expects a PUT request to /food/{id}
    await api.put(`/food/${currentEditingFood.value.id}`, currentEditingFood.value);
    modifyFoodMessage.value = 'Gericht erfolgreich aktualisiert!';
    // After saving, go back to the manage menu list and refresh it
    await toggleManageMenu();
  } catch (err) {
    console.error('Fehler beim Aktualisieren des Gerichts:', err);
    modifyFoodMessage.value = 'Fehler beim Aktualisieren. Bitte erneut versuchen.';
  }
};

// Function to cancel modifying a food item
const cancelModifyFood = () => {
  isModifyFood.value = false; // Hide the modify food form
  currentEditingFood.value = null; // Clear the editing food
  modifyFoodMessage.value = ''; // Clear messages
  toggleManageMenu(); // Go back to showing the list of food
};

// Function to delete a food item
const deleteFood = async (food) => {
  if (confirm(`Sind Sie sicher, dass Sie "${food.name}" löschen möchten?`)) {
    try {
      await api.delete(`/food/${food.id}`);
      foodList.value = foodList.value.filter(item => item.id !== food.id);
      foodLoadError.value = 'Gericht erfolgreich gelöscht!'; // Reusing for success message
      // Clear after a few seconds
      setTimeout(() => {
        foodLoadError.value = '';
      }, 3000);
    } catch (err) {
      console.error('Fehler beim Löschen des Gerichts:', err);
      foodLoadError.value = 'Fehler beim Löschen. Bitte erneut versuchen.';
    }
  }
};




</script>

<style scoped>
/* Custom styles for the sidebar navigation */
.sidebar .nav-link {
  font-size: 1.0rem;
  text-align: left;
}

.sidebar .nav-link.active,
.sidebar .nav-link:hover {
  margin: 10px;
  background-color: #fd7e14;
  color: white !important;
}

/* Styles for Restaurant Image Section */
.restaurant-image-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    margin-bottom: 30px;
    padding: 20px;
    background-color: #f8f9fa; /* Light background */
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.restaurant-image-section h4 {
    margin-top: 0;
    margin-bottom: 15px;
    color: #333;
    width: 100%;
    text-align: center;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
}

.restaurant-image-container {
    width: 200px; /* Fixed width for image display */
    height: 200px; /* Fixed height for image display */
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden; /* Hide overflow if image is larger */
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #fff;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    flex-shrink: 0; /* Prevent it from shrinking */
}

.restaurant-display-image {
    max-width: 100%;
    max-height: 100%;
    object-fit: cover; /* Cover the container while maintaining aspect ratio */
}

.restaurant-image-placeholder {
    width: 100%; /* Take full width of container */
    height: 100%; /* Take full height of container */
    border-radius: 50%; /* Make it circular within the container */
    background-color: #e9ecef; /* Lighter gray for placeholder */
    border: 2px dashed #adb5bd; /* Slightly darker dashed border */
    display: flex;
    justify-content: center;
    align-items: center;
    color: #6c757d; /* Darker text */
    font-size: 1em;
    text-align: center;
}

.image-upload-controls {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    align-items: center;
    width: 100%; /* Take full width within its parent */
    margin-top: 10px; /* Spacing from the image */
}

/* Bootstrap button classes are used directly in template, so minimal custom overrides */
.btn {
  font-weight: bold;
  min-width: 100px; /* Ensure consistent button size */
}

.btn:disabled {
  opacity: 0.6 !important;
  cursor: not-allowed !important;
}

/* Custom styles for the main content card for Restaurant Info */
.restaurant-info-management-container {
    max-width: 800px; /* Adjust width as desired */
    margin: 50px auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.restaurant-info-management-container .card-header h3 {
    margin-bottom: 0; /* No bottom margin for header text */
    text-align: center;
    color: #555;
    font-size: 1.25rem;
}

/* Styles for Read-Only Restaurant Details */
.restaurant-details-display {
    padding: 20px;
    background-color: #fff;
    border-radius: 6px;
    box-shadow: 0 1px 5px rgba(0,0,0,0.05);
}

.restaurant-details-display h4 {
    margin-top: 0;
    margin-bottom: 10px;
    color: #555;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
}

.restaurant-details-display p {
    margin-bottom: 8px;
    line-height: 1.6;
}

.restaurant-details-display p strong {
    min-width: 120px; /* Align labels */
    display: inline-block;
}

.restaurant-details-display a {
    color: #007bff;
    text-decoration: none;
}

.restaurant-details-display a:hover {
    text-decoration: underline;
}

/* General Layout for Main Content Cards */
.content > .card {
    margin-bottom: 25px; /* Spacing between different cards */
}

/* Messages (Bootstrap utility classes) */
.text-success { margin-top: 10px; text-align: center; width: 100%; }
.text-danger { margin-top: 10px; text-align: center; width: 100%; }

/* Media Queries for responsiveness */
@media (max-width: 767.98px) {
  main {
    padding-top: 1.5rem;
  }
}
.sidebar {
  height: auto;
  max-height: none;
  overflow-y: visible;
}
@media (min-width: 768px) {
  .sidebar {
    height: 100vh;
    max-height: 100vh;
    overflow-y: auto;
  }
}
</style>

<style scoped>
/* Custom styles for the sidebar navigation */
.sidebar .nav-link {
  font-size: 1.1rem;
  text-align: left;
}

.sidebar .nav-link.active,
.sidebar .nav-link:hover {
  background-color: #fd7e14;
  color: white !important;
}

.restaurant-image-container {
    text-align: center; /* Center content */
    margin-bottom: 20px;
    border: 1px solid #eee;
    padding: 10px;
    border-radius: 8px;
    background-color: #fff;
    display: flex; /* Use flexbox to easily center content */
    justify-content: center; /* Horizontally center */
    align-items: center; /* Vertically center */
    min-height: 150px; /* Give it a minimum height to make the circle visible */
}

.restaurant-display-image {
    max-width: 100%;
    height: auto;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

/* New styles for the placeholder circle */
.restaurant-image-placeholder {
    width: 160px; /* Adjust size as needed */
    height: 160px; /* Keep same as width for a perfect circle */
    border-radius: 50%; /* Makes it a circle */
    background-color: #f0f0f0; /* Light background color */
    border: 2px dashed #ccc; /* Dashed border to indicate placeholder */
    display: flex; /* Use flexbox to center text inside */
    justify-content: center;
    align-items: center;
    color: #888; /* Text color */
    font-size: 0.9em; /* Smaller font for "No Image" */
    text-align: center;
    flex-shrink: 0; /* Prevent it from shrinking if content is too wide */
}


/* Ensure content has some space at the top on small screens */
@media (max-width: 767.98px) {
  main {
    padding-top: 1.5rem;
  }
}
.sidebar {
  /* Default: small screens, sidebar height fits content */
  height: auto;
  max-height: none;
  overflow-y: visible;
}

/* On medium and larger screens, fixed full viewport height with scroll */
@media (min-width: 768px) {
  .sidebar {
    height: 100vh;
    max-height: 100vh;
    overflow-y: auto;
  }
}
</style>