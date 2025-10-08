<template>
    <div class="chef-info-container">
      <h1 class="chef-info-title">Koch Information</h1>
      <form @submit.prevent="submitForm" novalidate ref="form">
        <!-- Koch Name -->
        <div class="mb-3">
          <label for="kochName" class="form-label">Koch Name <span class="required-star">*</span></label>
          <input
            v-model="kochName"
            type="text"
            id="kochName"
            class="form-control"
            :class="{ 'is-invalid': errors.kochName }"
            placeholder="Koch Name"
            required
          />
          <div v-if="errors.kochName" class="invalid-feedback">Bitte gib den Kochnamen ein.</div>
        </div>
  
        <!-- Telefonnummer -->
        <div class="mb-3">
          <label for="telfone" class="form-label">Telefonnummer <span class="required-star">*</span></label>
          <input
            v-model="telfone"
            type="tel"
            id="telfone"
            class="form-control"
            :class="{ 'is-invalid': errors.telfone }"
            placeholder="Telefonnummer"
            required
            pattern="^\d{10}$"
          />
          <div v-if="errors.telfone" class="invalid-feedback">Bitte gib eine gültige Telefonnummer ein (z. B. 1234567890).</div>
        </div>
  
        <!-- Beschreibung -->
        <div class="mb-3">
          <label for="beschreibung" class="form-label">Beschreibung <span class="required-star">*</span></label>
          <input
            v-model="beschreibung"
            type="text"
            id="beschreibung"
            class="form-control"
            :class="{ 'is-invalid': errors.beschreibung }"
            placeholder="Beschreibung"
            required
          />
          <div v-if="errors.beschreibung" class="invalid-feedback">Bitte gib eine Beschreibung ein.</div>
        </div>
        <!-- cuisine -->
         <div class="mb-3">
          <label for="cuisine" class="form-label">Küche <span class="required-star">*</span>
          </label>
          <select v-model="selectedCuisine" class="form-control" @change="resetCustomCuisine">
            <option disabled value="">-- Wähle eine Küche --</option>
            <option v-for="cuisine in cuisines" :key="cuisine.id" :value="cuisine.cuisine_name">
              {{ cuisine.cuisine_name }}
           </option>
           <option value="custom">Andere (bitte eingeben)</option>  
          </select>
          <!-- Eingabefeld für eigene Cuisine erscheint nur, wenn "Andere" gewählt wird -->
          <input v-if="selectedCuisine === 'custom'" v-model="customCuisine" type="text" class="form-control mt-2" placeholder="Neue Küche eingeben" required/>
         </div>
  
        <!-- Adresse -->
        <div class="mb-3">
          <label class="form-label">Adresse <span class="required-star">*</span></label>
          <div class="address-fields">
            <input
              v-model="address.street"
              type="text"
              id="street"
              class="form-control"
              :class="{ 'is-invalid': errors.street }"
              placeholder="Straße"
              required
            />
            <input
              v-model="address.city"
              type="text"
              id="city"
              class="form-control"
              :class="{ 'is-invalid': errors.city }"
              placeholder="Stadt"
              required
            />
            <input
              v-model="address.postal_code"
              type="text"
              id="postal_code"
              class="form-control"
              :class="{ 'is-invalid': errors.postal_code }"
              placeholder="PLZ"
              required
            />
            <input
              v-model="address.flat_number"
              type="text"
              id="flat_number"
              class="form-control"
              placeholder="Stockwerk (optional)"
            />
            <input
              v-model="address.door_number"
              type="text"
              id="door_number"
              class="form-control"
              placeholder="Türnummer (optional)"
            />
          </div>
          <div v-if="errors.street || errors.city || errors.postal_code" class="invalid-feedback">
            Bitte fülle alle Adressfelder aus (Stockwerk & Türnummer sind optional).
          </div>
        </div>
  
        <!-- Bild-Upload -->
        <div class="mb-3">
          <label for="image" class="form-label">Profilbild</label>
          <input
            type="file"
            id="image"
            class="form-control"
            @change="handleImageUpload"
            accept="image/png, image/jpeg, image/gif"
            required
          />
          <div class="invalid-feedback">Bitte wähle ein Bild aus (JPG, PNG, GIF).</div>
        </div>
  
        <div v-if="imagePreview" class="mb-3">
          <label class="form-label">Bildvorschau</label>
          <img :src="imagePreview" alt="Bildvorschau" class="img-fluid" style="max-width: 200px;" />
        </div>
  
        <button type="submit">Registrieren</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        kochName: "",
        telfone: "",
        beschreibung: "",
        address: {
          street: "",
          city: "",
          postal_code: "",
          flat_number: "",
          door_number: "",
        },
        image: null,
        imagePreview: null,
        errors: {},
        cuisines: [
          { id: 1, cuisine_name: "Italienisch" },
          { id: 2, cuisine_name: "Chinesisch" },
          { id: 3, cuisine_name: "Indisch" },
          { id: 4, cuisine_name: "Mexikanisch" },
          { id: 5, cuisine_name: "Arabiesch" },
          { id: 5, cuisine_name: "Persisch" },
          { id: 5, cuisine_name: "Österreichisch" },
        ], 
        selectedCuisine: "", // Vom Koch gewählte Cuisine
        customCuisine: "", // Falls der Koch eine eigene Cuisine eingibt
      };
    },
    methods: {
      resetCustomCuisine() {
        if (this.selectedCuisine !== "custom") {
          this.customCuisine = "";
        }
      },
      submitForm() {
        this.errors = {};
  
        // Name prüfen
        if (!this.kochName) {
          this.errors.kochName = true;
        }
  
        // Telefonnummer prüfen
        const phoneRegex = /^\d{10}$/;
        if (!this.telfone || !phoneRegex.test(this.telfone)) {
          this.errors.telfone = true;
        }
  
        // Beschreibung prüfen
        if (!this.beschreibung) {
          this.errors.beschreibung = true;
        }
  
        // Adresse prüfen
        if (!this.address.street) {
          this.errors.street = true;
        }
        if (!this.address.city) {
          this.errors.city = true;
        }
        if (!this.address.postal_code) {
          this.errors.postal_code = true;
        }
  
        // Falls es Fehler gibt, abbrechen
        if (Object.keys(this.errors).length > 0) {
          return;
        }
  
        // Falls alles passt, Formular absenden
        console.log({
          kochName: this.kochName,
          telfone: this.telfone,
          beschreibung: this.beschreibung,
          address: this.address,
          image: this.image,
        });
  
        alert("Formular erfolgreich gesendet!");
      },
  
      handleImageUpload(event) {
        const file = event.target.files[0];
  
        if (file && file.size < 5 * 1024 * 1024 && ["image/jpeg", "image/png", "image/gif"].includes(file.type)) {
          this.image = file;
  
          const reader = new FileReader();
          reader.onload = (e) => {
            this.imagePreview = e.target.result;
          };
          reader.readAsDataURL(file);
        } else {
          alert("Bitte wähle ein gültiges Bild (JPG, PNG oder GIF) mit max. 5MB.");
          this.imagePreview = null;
          this.image = null;
        }
      },
    },
  };
  </script>
  
  <style lang="scss" scoped>
  @use "@/assets/_button.scss" as *;
  
  .chef-info-container {
    padding: 20px;
  }
  
  .chef-info-title {
    font-size: 2rem;
    margin-bottom: 20px;
    color: #333;
  }
  
  input:focus,
  textarea:focus,
  select:focus {
    border-color:#ffaa33;
    box-shadow: 0 0 10px rgba(255, 186, 88, 0.5);
    outline: none; // Entfernt den Standard-Fokus-Ring
  }
  .mb-3 {
    margin-bottom: 1.5rem;
  }
  
  .form-label {
    font-size: 1.1rem;
  }
  
  .address-fields {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }
  
  .invalid-feedback {
    display: block;
    color: red;
    font-size: 0.875rem;
  }
  
  .btn {
    @extend button;
    margin-top: 15px;
  }
  </style>
  