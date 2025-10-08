<template>
    <div class="container mt-5">
       
      <div class="row">
        <!-- Left column: Chef info & foods (3/4) -->
        <div class="col-md-9">
          <!-- Chef Card -->
          
            <div class="card mb-4 shadow-sm chef-info-card text-white">
                <div class="card-body bg-overlay text-center">
                    <h4 class="card-title">{{ chef.name }}</h4>
                    <p>{{ chef.description }}</p>
                    <p><strong>City:</strong> {{ chef.city }}</p>
                    <p><strong>Cuisine:</strong> {{ chef.cuisine }}</p>
                    <p><strong>Special:</strong> {{ chef.specialFeatures.join(', ') }}</p>
                    <p><strong>Rating:</strong> {{ chef.rating }}</p>
                    <div class="d-flex gap-2">
                    <button class="btn btn-success" @click="makeReservation">Reserve</button>
                    </div>
            </div>
        </div>
  
          <!-- Food List -->
          <h5>Available Foods</h5>
          <div v-for="food in chef.foods" :key="food.id" class="card mb-3 shadow-sm">
            <div class="card-body">
              <h5 class="card-title">{{ food.name }}</h5>
              <p><strong>Price:</strong> ${{ food.price.toFixed(2) }}</p>
              <p><strong>Special:</strong> {{ food.specialFeatures.join(', ') }}</p>
              <p><strong>Ingredients:</strong> {{ food.ingredients.join(', ') }}</p>
              <button class="btn btn-outline-primary" @click="addToCart(food)">Add to Basket</button>
            </div>
          </div>
        </div>
  
        <!-- Right column: Basket (1/4) -->
        <div class="col-md-3">
          <div class="basket card shadow sticky-top">
            <div class="card-header bg-primary text-white text-center">
              <h5>Your Basket</h5>
            </div>
            <div class="card-body" style="max-height: 70vh; overflow-y: auto;">
              <div v-if="cart.length > 0">
                <div v-for="(item, index) in cart" :key="item.food.id" class="mb-3 border-bottom pb-2">
                  <strong>{{ item.food.name }}</strong>
                  <p>${{ item.food.price.toFixed(2) }} x {{ item.quantity }}</p>
                  <div class="d-flex align-items-center">
                    <button class="btn btn-sm btn-danger me-2" @click="decreaseQuantity(index)">−</button>
                    <span>{{ item.quantity }}</span>
                    <button class="btn btn-sm btn-success ms-2" @click="increaseQuantity(index)">+</button>
                  </div>
                </div>
                <hr>
                <p><strong>Total:</strong> ${{ totalPrice.toFixed(2) }}</p>
                <button class="btn btn-success w-100" @click="confirmOrder">Confirm</button>
              </div>
              <div v-else class="text-center text-muted mt-3">
                Your basket is empty
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Reservation Modal -->
      <div class="modal fade" id="reservationModal" tabindex="-1" aria-labelledby="reservationModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="reservationModalLabel">Reserve with {{ chef.name }}</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <label for="reservationDate" class="form-label">Select a date:</label>
              <input type="date" class="form-control" id="reservationDate" v-model="reservationDate">
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
              <button type="button" class="btn btn-success" @click="submitReservation">Confirm Reservation</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import data from '../../assets/data.json';
  
  import Navigation from '@/components/TheNavigation.vue';

   export default {
    components: {
    Navigation
  },
    data() {
      return {
        chef: {},
        cart: [],
        reservationDate: ''
      };
    },
    created() {
      const chefId = this.$route.params.id;
      this.chef = data.chefs.find(chef => chef.id === parseInt(chefId));
    },
    computed: {
      totalPrice() {
        return this.cart.reduce((sum, item) => sum + item.food.price * item.quantity, 0);
      }
    },
    methods: {
      makeReservation() {
        const modal = new bootstrap.Modal(document.getElementById('reservationModal'));
        modal.show();
      },
      submitReservation() {
        if (!this.reservationDate) {
          alert("Please select a date.");
          return;
        }
        alert(`Reservation confirmed for ${this.chef.name} on ${this.reservationDate}`);
        this.reservationDate = '';
        const modalElement = document.getElementById('reservationModal');
        const modal = bootstrap.Modal.getInstance(modalElement);
        modal.hide();
      },
      placeOrder() {
        alert(`Order placed with Chef ${this.chef.name}`);
      },
      addToCart(food) {
        const existingItem = this.cart.find(item => item.food.id === food.id);
        if (existingItem) {
          existingItem.quantity++;
        } else {
          this.cart.push({ food, quantity: 1 });
        }
      },
      increaseQuantity(index) {
        this.cart[index].quantity++;
      },
      decreaseQuantity(index) {
        if (this.cart[index].quantity > 1) {
          this.cart[index].quantity--;
        } else {
          this.cart.splice(index, 1);
        }
      },
      confirmOrder() {
        alert('Order confirmed!');
        this.cart = [];
      }
    }
  };
  </script>
  
  <style scoped>
  .chef-info-card {
  background-image: url('/images/36129.jpg');
  background-size: cover;
  background-position: center;
  border-radius: 12px;
  overflow: hidden;
  position: relative;
  color: white;
}

.bg-overlay {
  background-color: rgba(0, 0, 0, 0.5); /* semi-transparent dark overlay */
  padding: 1.5rem;
  border-radius: 12px;
}
  .basket {
    border: 2px solid #007bff;
    border-radius: 12px;
    font-size: 1.1rem;
  }
  .sticky-top {
    top: 20px;
  }
  .card-header {
    border-bottom: 1px solid #ddd;
  }
  </style>
  