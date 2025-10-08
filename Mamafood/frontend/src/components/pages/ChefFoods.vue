<template>
  <div class="container">
    <h2>Food of {{ chef?.name || 'chef' }}</h2>

    <div v-if="loading">Loading…</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else>
      <article v-for="f in foods" :key="f.id" class="card">
        <h3>{{ f.name }}</h3>
        <p>Price: {{ money(f.price) }}</p>
        <button @click="addToBasket(f)">Add to basket</button>
      </article>

      <p v-if="!foods.length">no food</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/utils/axios' // همون اینستنس اکسیوس خودت

const route = useRoute()
const chefId = route.params.chefId

const chef = ref(null)
const foods = ref([])
const loading = ref(true)
const error = ref('')

const money = (v) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'EUR' })
    .format(v ?? 0)

const addToBasket = (f) => {
  // TODO: اضافه به سبد خرید
  console.log('add to basket', f)
}

onMounted(async () => {
  try {
    // آدرس‌ها را با API خودت هماهنگ کن
    const chefRes = await api.get(`/restaurant/${chefId}/`)
    const foodsRes = await api.get(`/food/food_restaurant_id/${chefId}`)

    chef.value = chefRes.data
    foods.value = foodsRes.data
  } catch (e) {
    error.value = 'error in loading'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.container { max-width: 1000px; margin: 0 auto; padding: 16px; }
.card { border: 1px solid #eee; padding: 12px; border-radius: 12px; margin-bottom: 10px; }
.error { color: #b00; }
</style>
