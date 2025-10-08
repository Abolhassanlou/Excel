<template>
  <div class="welcome">
    <NavBar />
    <div class="hero">
      <img :src="slides[currentIndex].image" alt="Willkommen" class="slide-image" />
      <div class="slide-text">
        <h1>{{ slides[currentIndex].text }}</h1>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const slides = ref([
  { text: "Willkommen bei Mama Food! Frisch. Lecker. Hausgemacht.", image: "/images/home.png" },
  { text: "Authentische Gerichte – direkt aus heimischen Küchen!", image: "/images/images.jpeg" },
  { text: "Koche & verdiene von Zuhause – starte jetzt!", image: "/images/Download.jpeg" },
]);

const currentIndex = ref(0);

const changeSlide = () => {
  currentIndex.value = (currentIndex.value + 1) % slides.value.length;
};

onMounted(() => {
  setInterval(changeSlide, 30000); // Ändert das Bild alle 30 Sekunden
});
</script>

<style scoped>
.welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.hero {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 400px; 
  background: rgba(255, 255, 255, 0.8);
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  margin: 50px ;
  margin-top: 200px;
}

.slide-image {
  width: 60%;
  height: 100%;
  object-fit: contain;
  border-radius: 10px;
}

.slide-text {
  width: 40%;
  padding-left: 20px;
  text-align: left;
}

.slide-text h1 {
  font-size: 1.8rem;
  color: #333;
}
</style>