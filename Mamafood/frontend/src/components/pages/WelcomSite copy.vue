<template>
  <div id="app" class="container my-4">
    <header class="bg-success text-white p-4 mb-4 d-flex justify-content-between align-items-center">
      <div>
        <h1 class="mb-0">Chef's Table</h1>
        <p class="mb-0">Discover amazing dishes from talented chefs near you.</p>
      </div>
      <div class="account">Account</div>
    </header>

    <div class="row g-2 mb-4">
      <div class="col-md">
        <input type="text" class="form-control" placeholder="Enter chef name..." v-model="searchName" />
      </div>
      <div class="col-md">
        <select class="form-select" v-model="filterCity">
          <option value="">All Cities</option>
          <option v-for="city in uniqueCities" :key="city" :value="city">{{ city }}</option>
        </select>
      </div>
      <div class="col-md">
        <select class="form-select" v-model="filterCuisine">
          <option value="">All Cuisines</option>
          <option v-for="cuisine in uniqueCuisines" :key="cuisine" :value="cuisine">{{ cuisine }}</option>
        </select>
      </div>
    </div>

    <div class="row mb-4">
      <div class="col-md-4">
        <div class="card p-3">
          <h2>Your Order</h2>
          <p v-if="order.length === 0">Your order is empty.</p>
          <ul class="list-group" v-else>
            <li class="list-group-item d-flex flex-column" v-for="(orderItem, index) in order" :key="orderItem.item.id">
              <strong>{{ orderItem.item.name }}</strong>
              <div class="d-flex align-items-center mt-2">
                <button class="btn btn-sm btn-outline-secondary me-2" @click="decreaseQuantity(index)">-</button>
                <span>{{ orderItem.quantity }}</span>
                <button class="btn btn-sm btn-outline-secondary ms-2" @click="increaseQuantity(index)">+</button>
                <span class="ms-3">x ${{ (orderItem.item.price * orderItem.quantity).toFixed(2) }}</span>
                <button class="btn btn-sm btn-outline-danger ms-2" @click="removeFromOrder(index)">x</button>
              </div>
            </li>
          </ul>
          <p class="mt-3"><strong>Total: ${{ total.toFixed(2) }}</strong></p>
          <button class="btn btn-success w-100" :disabled="order.length === 0 || isOrderProcessing" @click="placeOrderDemo">
            Place Order (Demo)
          </button>
        </div>
      </div>

      <div class="col-md-8">
        <div>
          <h2>Menu & Reservation</h2>
          <div v-if="orderedChef" class="mb-3">
            <h3>{{ orderedChef }}'s Menu</h3>
            <div class="border p-3 rounded bg-light">
              <p>Reserve {{ orderedChef }} for a Special Day</p>
              <div class="mb-2">
                <label for="select-date" class="form-label">Select Date:</label>
                <input type="date" id="select-date" class="form-control" />
              </div>
              <button class="btn btn-secondary" disabled>Reserve Date (Demo)</button>
            </div>
          </div>
          <h2 class="mt-4">All Available Menu Items</h2>
          <div class="row row-cols-1 row-cols-md-2 g-3">
            <div class="col" v-for="item in filteredMenuItemsByChef" :key="item.id">
              <div class="card h-100 p-3">
                <h3>{{ item.name }}</h3>
                <p class="text-muted">{{ item.chef }}</p>
                <p>{{ item.description }}</p>
                <p><strong>${{ item.price.toFixed(2) }}</strong></p>
                <button class="btn btn-primary mt-auto" @click="addToOrder(item)">Add to Order</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div>
      <h2>Our Chefs</h2>
      <div class="d-flex align-items-center mb-3">
        <label class="me-2">Sort by:</label>
        <select class="form-select w-auto" v-model="sortBy">
          <option value="name">Name (A-Z)</option>
          <option value="rating">Rating (High to Low)</option>
        </select>
      </div>
      <div class="row row-cols-1 row-cols-md-3 g-3">
        <div class="col" v-for="chef in sortedChefs" :key="chef.name">
          <div class="card p-3">
            <h3>{{ chef.name }}</h3>
            <p>{{ chef.cuisine }} - {{ chef.location }}</p>
            <div>
              <span v-for="i in chef.rating" :key="'star-' + i">⭐</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showOrderConfirmation" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content p-3">
          <div class="modal-header">
            <h5 class="modal-title">Order Confirmation</h5>
            <button type="button" class="btn-close" @click="closeConfirmationWithoutClear"></button>
          </div>
          <div class="modal-body">
            <p>Order Placed (Demo)!</p>
            <p><strong>Chef:</strong> {{ orderedChef }}</p>
            <p><strong>Items:</strong></p>
            <ul>
              <li v-for="orderItem in order" :key="orderItem.item.id">
                - {{ orderItem.item.name }} x {{ orderItem.quantity }} (${{(orderItem.item.price * orderItem.quantity).toFixed(2)}})
              </li>
            </ul>
            <p><strong>Total: ${{ total.toFixed(2) }}</strong></p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-primary" @click="closeOrderConfirmation">OK</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import data from '../../assets/data.json';

export default {
  data() {
    return {
      chefs: data.chefs,
      menuItems: data.menuItems,
      order: [],
      searchName: '',
      filterCity: '',
      filterCuisine: '',
      sortBy: 'name',
      orderedChef: null,
      showOrderConfirmation: false,
      isOrderProcessing: false
    };
  },
  computed: {
    uniqueCities() {
      return [...new Set(this.chefs.map(chef => chef.location))];
    },
    uniqueCuisines() {
      return [...new Set(this.menuItems.map(item => item.cuisine))];
    },
    filteredMenuItems() {
      return this.menuItems.filter(item => {
        const nameMatch = item.name.toLowerCase().includes(this.searchName.toLowerCase());
        const cuisineMatch = !this.filterCuisine || item.cuisine === this.filterCuisine;
        return nameMatch && cuisineMatch;
      });
    },
    filteredMenuItemsByChef() {
      if (this.orderedChef) {
        return this.filteredMenuItems.filter(item => item.chef === this.orderedChef);
      }
      return this.filteredMenuItems;
    },
    filteredChefs() {
      return this.chefs.filter(chef => {
        const nameMatch = chef.name.toLowerCase().includes(this.searchName.toLowerCase());
        const cityMatch = !this.filterCity || chef.location === this.filterCity;
        return nameMatch && cityMatch;
      });
    },
    sortedChefs() {
      let sorted = [...this.filteredChefs];
      if (this.sortBy === 'name') {
        sorted.sort((a, b) => a.name.localeCompare(b.name));
      } else if (this.sortBy === 'rating') {
        sorted.sort((a, b) => b.rating - a.rating);
      }
      return sorted;
    },
    total() {
      return this.order.reduce((sum, orderItem) => sum + (orderItem.item.price * orderItem.quantity), 0);
    }
  },
  methods: {
    addToOrder(item) {
      const existingItemIndex = this.order.findIndex(orderItem => orderItem.item.id === item.id);
      if (existingItemIndex > -1) {
        this.order[existingItemIndex].quantity++;
      } else {
        this.order.push({ item: item, quantity: 1 });
        if (!this.orderedChef && this.order.length > 0) {
          this.orderedChef = item.chef;
        }
      }
    },
    increaseQuantity(index) {
      this.order[index].quantity++;
    },
    decreaseQuantity(index) {
      if (this.order[index].quantity > 1) {
        this.order[index].quantity--;
      }
    },
    removeFromOrder(index) {
      this.order.splice(index, 1);
      if (this.order.length === 0) {
        this.orderedChef = null;
      } else if (!this.orderedChef && this.order.length > 0) {
        this.orderedChef = this.order[0].item.chef;
      }
    },
    placeOrderDemo() {
      if (this.order.length > 0) {
        this.isOrderProcessing = true;
        this.showOrderConfirmation = true;
      } else {
        alert("Your order is empty!");
      }
    },
    closeOrderConfirmation() {
      this.showOrderConfirmation = false;
      this.isOrderProcessing = false;
      this.order = [];
      this.orderedChef = null;
    },
    closeConfirmationWithoutClear() {
      this.showOrderConfirmation = false;
      this.isOrderProcessing = false;
    }
  }
};
</script>
