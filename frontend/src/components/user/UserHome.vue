<template>
  <div class="container-fluid py-2">
    <h3 class="fw-bold mb-4">Welcome, {{ firstName }}!</h3>

    <div class="d-flex justify-content-between align-items-center mb-3">
      <h5 class="fw-bold mb-0">Available Treks</h5>
      <div class="d-flex gap-2">
        <select class="form-select form-select-sm" style="min-width: 130px;" :value="trekStore.filterDifficulty"
          @change="onFilterChange">
          <option value="">Difficulty: All</option>
          <option value="Easy">Easy</option>
          <option value="Moderate">Moderate</option>
          <option value="Hard">Hard</option>
        </select>
      </div>
    </div>

    <div class="row g-4 mb-2">
      <div class="col-md-4" v-for="trek in availableTreks.slice(0, 3)" :key="trek.id">
        <div class="card h-100 shadow-sm border-0 rounded-3 overflow-hidden">
          <img
            src="https://images.unsplash.com/photo-1551632811-561732d1e306?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dHJla2tpbmd8ZW58MHx8MHx8fDA%3D"
            class="card-img-top" alt="Trek" style="height: 180px; object-fit: cover;">
          <div class="card-body d-flex flex-column">
            <h5 class="card-title fw-bold mb-3">{{ trek.name }}</h5>
            <p class="text-dark mb-3">{{ trek.location }}</p>
            <p class="text-muted mb-3">{{ trek.difficulty }} : {{ trek.duration }} Days</p>
            <p class="text-dark mb-4">Slots Left: {{ trek.slots }}</p>

            <div class="mt-auto">
              <button v-if="trek.slots > 0" class="btn btn-outline-primary w-100 fw-bold rounded-2 py-2"
                @click="bookTrek(trek)">
                Book Now
              </button>
              <button v-else class="btn btn-light border w-100 fw-bold text-muted rounded-2 py-2" disabled>
                Not Available
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="d-flex justify-content-center mb-3">
      <router-link to="/user-dashboard/browse" class="btn btn-primary px-4 py-2 d-inline-flex align-items-center gap-2">
        Browse All
        <span aria-hidden="true">&rarr;</span>
      </router-link>
    </div>

    <div class="d-flex justify-content-between align-items-center mb-3">
      <h5 class="fw-bold mb-0">My Bookings</h5>
      <router-link to="/user-dashboard/bookings"
        class="text-decoration-none text-primary fw-bold d-flex align-items-center gap-1">
        View All Bookings <span aria-hidden="true">&rarr;</span>
      </router-link>
    </div>

    <div class="card shadow-sm border-0 rounded-3 overflow-hidden">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-borderless align-middle mb-0 text-center">
            <thead class="bg-light text-muted border-bottom">
              <tr>
                <th class="py-3 text-start ps-4 fw-semibold">Trek Name</th>
                <th class="py-3 fw-semibold">Booking Date</th>
                <th class="py-3 fw-semibold">Status</th>
                <th class="py-3 text-end pe-4 fw-semibold">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="booking in activeBookings" :key="booking.booking_id" class="border-bottom">
                <td class="text-start ps-4 fw-semibold text-dark">{{ booking.trek_name }}</td>
                <td class="text-dark">{{ booking.booking_date }}</td>
                <td class="text-dark">{{ booking.status }}</td>
                <td class="text-end pe-4">
                  <router-link to="/user-dashboard/bookings"
                    class="btn btn-sm btn-outline-primary fw-bold px-3 py-1 rounded-2">
                    View Details
                  </router-link>
                </td>
              </tr>
              <tr v-if="activeBookings.length === 0">
                <td colspan="4" class="py-4 text-muted">You have no active bookings right now.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useTrekStore } from '../../stores/trekStore' // 1. Import the store
import { useToast } from "vue-toastification"
import Swal from 'sweetalert2'

export default {
  // 2. Initialize the store for this component
  setup() {
    const trekStore = useTrekStore();
    const toast = useToast();
    return { trekStore, toast };
  },
  data() {
    return {
      availableTreks: [],
      myBookings: [],
      userFullName: ''
    }
  },
  computed: {
    activeBookings() {
      return this.myBookings.filter(b => b.status === 'Booked').slice(0, 3);
    },
    firstName() {
      if (!this.userFullName) return 'Trekker';
      return this.userFullName.split(' ')[0];
    }
  },
  mounted() {
    this.fetchProfile()
    this.fetchOpenTreks()
    this.fetchMyBookings()
  },
  methods: {
    async fetchProfile() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/user/profile')
        this.userFullName = res.data.full_name
      } catch (err) {
        // Silent fail
      }
    },
    async fetchOpenTreks() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/user/treks', {
          params: {
            // 3. Pull the difficulty filter from Pinia memory
            difficulty: this.trekStore.filterDifficulty
          }
        })
        this.availableTreks = res.data.treks || res.data
      } catch (err) {
        console.error("Failed to load treks")
      }
    },
    // 4. New method to update the store when the dropdown changes
    onFilterChange(event) {
      this.trekStore.updateDifficulty(event.target.value);
      this.fetchOpenTreks();
    },
    async fetchMyBookings() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/user/bookings')
        this.myBookings = res.data
      } catch (err) {
        // Silent fail
      }
    },
    async bookTrek(trek) {
      // 1. Ask for permission first
      const result = await Swal.fire({
        title: `Book ${trek.name}?`,
        text: `Are you sure you want to reserve a slot for this trek?`,
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#198754', // Bootstrap Success Green
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Yes, book it!'
      });

      // 2. Only proceed if they clicked Yes
      if (result.isConfirmed) {
        try {
          // Use trek.id for the API call
          await axios.post(`http://127.0.0.1:5000/api/user/book/${trek.id}`)

          this.toast.success("Trek booked successfully!")
          this.fetchOpenTreks()
          this.fetchMyBookings()
        } catch (err) {
          this.toast.error(err.response?.data?.message || 'Error booking trek.')
        }
      }
    }
  }
}
</script>

<style scoped>
/* Minor custom styling to enforce the exact border colors from the image */
.card {
  border: 1px solid #e9ecef !important;
}

.btn-outline-primary {
  border-width: 1.5px;
}
</style>