<template>
  <div class="container py-3">
    <div class="d-flex align-items-center gap-2 mb-3">
      <h1 class="h4 mb-0">Our Chefs</h1>
      <span v-if="loading" class="spinner-border spinner-border-sm" />
    </div>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-if="!loading && chefs.length === 0" class="alert alert-info">
      There is no chef    </div>

    <div v-for="chef in chefs" :key="chef.id" class="card mb-3">
      <div class="row g-0">
        <div class="col-4 col-sm-3 col-lg-2">
  <div class="ratio ratio-1x1 rounded-start overflow-hidden">
    <img
      :src="chef.photo"
      alt="Chef photo"
      class="w-100 h-100 object-fit-cover"
      loading="lazy"
    />
  </div>
</div>
        <div class="col-sm-9">
          <div class="card-body">
            <h5 class="card-title">{{ chef.name }}</h5>
            <p class="card-text" v-if="chef.description">{{ chef.description }}</p>
            <p class="mb-1"><strong>City:</strong> {{ chef.city || '-' }}</p>
            <p class="mb-1"><strong>Add:</strong> {{ chef.street || '-' }} {{ chef.flat_number || '-' }} /{{ chef.door_number || '-' }} P: {{ chef.postal_code || '-' }}  </p>
            <p class="mb-1"><strong>Cuisine:</strong> {{ chef.cuisine || '-' }}</p>
            <p class="mb-1" v-if="chef.tel"><strong>Tel:</strong> {{ chef.tel }}</p>
            <p class="mb-1" v-if="chef.pickup_time"><strong>Pickup:</strong> {{ chef.pickup_time }}</p>

            <router-link
              :to="{ name: 'chef', params: { id: chef.id } }"
              class="btn btn-primary btn-sm mt-2"
            >
              View Profile
            </router-link>
            <a
  :href="`${baseURL}/restaurant/${chef.id}`"
  target="_blank"
  class="btn btn-outline-secondary btn-sm mt-2 ms-2"
>
  Test API
</a>
          </div>
        </div>
      </div>
    </div>

    <!-- فاز ۲: اینجا بعداً فیلترها اضافه می‌شوند -->
  </div>
</template>

<script>
import axios from 'axios';
import api , { BASE_URL } from '@/utils/axios'; // Your Axios instance




/*const api = axios.create({
  baseURL: BASE_URL
});*/

export default {
  name: 'ChefsList',
  data() {
    return {
      loading: false,
      error: '',
      cuisineMap: new Map(), // id -> cuisine_name
      addressMap: new Map(), // id -> { city, ... }
      chefs: []
    };
  },
  mounted() {
    this.loadPhaseOne();
  },
  computed: {
    baseURL() {
      return api.defaults.baseURL;
    }
  },
  methods: {
    async loadPhaseOne() {
      this.loading = true;
      this.error = '';
      try {
        // موازی: رستوران‌ها + کیوزین‌ها + آدرس‌ها
        const [restRes, cuisineRes, addrRes] = await Promise.all([
          api.get('/restaurant/all/'),
          api.get('/cuisine/all/'), // [{ id, cuisine_name }]
          api.get('/address/all/')  // [{ id, city, ... }]
        ]);

        const cuisines = Array.isArray(cuisineRes.data) ? cuisineRes.data : (cuisineRes.data?.data ?? []);
        cuisines.forEach(c => this.cuisineMap.set(Number(c.id), c.cuisine_name));

        const addresses = Array.isArray(addrRes.data) ? addrRes.data : (addrRes.data?.data ?? []);
        addresses.forEach(a => this.addressMap.set(Number(a.id), a));

        const restaurants = Array.isArray(restRes.data) ? restRes.data : (restRes.data?.data ?? []);
        this.chefs = restaurants.map(this.normalizeRestaurant);
      } catch (e) {
        this.error = 'error getting info from back end';
      } finally {
        this.loading = false;
      }
    },

    normalizeRestaurant(r) {
      const cuisineName = this.cuisineMap.get(Number(r.cuisine_id)) || '';
      const addr = this.addressMap.get(Number(r.address_id)) || {};
      const cityName = this.titleCase(addr.city || '');
      const Street = this.titleCase(addr.street || '');
      const flat_number = this.titleCase(addr.flat_number || '');
      const door_number = this.titleCase(addr.door_number || '');
      const postal_code = this.titleCase(addr.postal_code || '');
      
      
      

      const photo = r.image_url
        ? (String(r.image_url).startsWith('http') ? r.image_url : `${BASE_URL}${r.image_url}`)
        : 'https://via.placeholder.com/400x300?text=Chef';

      return {
        id: r.id ?? r.user_id,
        name: r.restaurant_name || `Chef #${r.user_id ?? r.id}`,
        description: r.description || '',
        city: cityName,
        street: Street,
        flat_number :flat_number ,
        door_number:door_number,
        postal_code:postal_code,

        cuisine: cuisineName,
        tel: r.tel_number || '',
        pickup_time: r.pickup_time || '',
        photo
      };
    },

    titleCase(s) {
      if (!s) return s;
      const lower = String(s).toLowerCase();
      return lower.replace(/\b\p{L}/gu, ch => ch.toUpperCase());
    }
  }
};
</script>

<style scoped>
.object-fit-cover { object-fit: cover; }
</style>
