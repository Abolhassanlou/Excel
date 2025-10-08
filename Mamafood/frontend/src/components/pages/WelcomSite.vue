<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Sidebar Filters -->
      <aside class="col-md-3 bg-light p-3">
        <h2 class="h5 mb-3">Filter Chefs</h2>

        <!-- City Filter -->
        <div class="mb-3">
          <label class="form-label fw-bold">City</label>
          <select v-model="filters.city" class="form-select">
            <option value="">All Cities</option>
            <option v-for="city in uniqueCities" :key="city">{{ city }}</option>
          </select>
        </div>

        <!-- Cuisine Type Filter -->
        <div class="mb-3">
          <label class="form-label fw-bold">Cuisine Type</label>
          <select v-model="filters.cuisine" class="form-select">
            <option value="">All Cuisines</option>
            <option v-for="type in uniqueCuisines" :key="type">{{ type }}</option>
          </select>
        </div>

        <!-- Special Features Filter -->
        <div class="mb-3">
          <label class="form-label fw-bold">Special Features</label>
          <div v-for="feature in uniqueFeatures" :key="feature" class="form-check">
            <input type="checkbox" :value="feature" v-model="filters.specialFeatures" class="form-check-input" />
            <label class="form-check-label">{{ feature }}</label>
          </div>
        </div>

        <!-- Rating Filter -->
        <div class="mb-3">
          <label class="form-label fw-bold">Minimum Rating</label>
          <input type="range" v-model="filters.rating" min="0" max="5" step="0.5" class="form-range" />
          <span>{{ filters.rating }}+</span>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="col-md-9 p-3">
        <h1 class="h3 mb-4">Our Chefs</h1>
        <div v-for="chef in filteredChefs" :key="chef.id" class="card mb-4">
          <div class="row g-0">
            <!-- Image Column -->
            <div class="col-md-3">
              <img :src="chef.photo" alt="Chef photo" class="img-fluid rounded-start h-100 w-100 object-fit-cover" />
            </div>

            <!-- Info Column -->
            <div class="col-md-9">
              <div class="card-body">
                <h5 class="card-title">{{ chef.name }}</h5>
                <p class="card-text">{{ chef.description }}</p>
                <p><strong>City:</strong> {{ chef.city }}</p>
                <p><strong>Cuisine:</strong> {{ chef.cuisine }}</p>
                <p><strong>Special:</strong> {{ chef.specialFeatures.join(', ') }}</p>
                <p><strong>Rating:</strong> {{ chef.rating }}</p>
                <router-link :to="{ name: 'chef', params: { id: chef.id } }" class="btn btn-primary">View Profile</router-link>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import data from '../../assets/data.json';

export default {
  data() {
    return {
      filters: {
        city: '',
        cuisine: '',
        specialFeatures: [],
        rating: 0
      },
      chefs: data.chefs || []
    };
  },
  computed: {
    uniqueCities() {
      return [...new Set(this.chefs.map(c => c.city))];
    },
    uniqueCuisines() {
      return [...new Set(this.chefs.map(c => c.cuisine))];
    },
    uniqueFeatures() {
      return [...new Set(this.chefs.flatMap(c => c.specialFeatures))];
    },
    filteredChefs() {
      return this.chefs.filter(chef => {
        return (
          (!this.filters.city || chef.city === this.filters.city) &&
          (!this.filters.cuisine || chef.cuisine === this.filters.cuisine) &&
          (this.filters.specialFeatures.length === 0 || this.filters.specialFeatures.every(f => chef.specialFeatures.includes(f))) &&
          chef.rating >= this.filters.rating
        );
      });
    }
  }
};
</script>

<style scoped>
.object-fit-cover {
  object-fit: cover;
}
/* Bootstrap handles most layout/styling */
</style>
