<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Trekker Dashboard</h2>
      <button class="btn btn-outline-danger" @click="logout">Logout</button>
    </div>

    <div v-if="message" class="alert" :class="isError ? 'alert-danger' : 'alert-success'">
      {{ message }}
    </div>

    <div class="row">
      <div class="col-md-7">
        <div class="card shadow-sm mb-4">
          <div class="card-header bg-success text-white">Explore Available Treks</div>
          <div class="card-body bg-light">

            <div class="row mb-3">
              <div class="col-md-7">
                <input type="text" class="form-control" placeholder="Search by name or location..."
                  v-model="searchQuery" @input="fetchOpenTreks">
              </div>
              <div class="col-md-5">
                <select class="form-select" v-model="filterDifficulty" @change="fetchOpenTreks">
                  <option value="">All Difficulties</option>
                  <option value="Easy">Easy</option>
                  <option value="Moderate">Moderate</option>
                  <option value="Hard">Hard</option>
                </select>
              </div>
            </div>

            <div class="list-group">
              <div v-for="trek in availableTreks" :key="trek.id"
                class="list-group-item list-group-item-action d-flex justify-content-between align-items-center mb-2 shadow-sm rounded">
                <div>
                  <h5 class="mb-1">{{ trek.name }}</h5>
                  <p class="mb-1 text-muted"><small>📍 {{ trek.location }} | ⏱️ {{ trek.duration }} days | ⛰️ {{
                    trek.difficulty }}</small></p>
                  <small class="text-success fw-bold">{{ trek.slots }} slots left</small>
                </div>
                <button class="btn btn-primary" @click="bookTrek(trek.id)">Book Now</button>
              </div>
              <div v-if="availableTreks.length === 0" class="text-center py-4 text-muted">
                No treks match your search criteria right now.
              </div>
            </div>

          </div>
        </div>
      </div>

      <div class="col-md-5">
        <div class="card shadow-sm">
          <div class="card-header bg-dark text-white">My Booking History</div>
          <div class="card-body p-0">
            <table class="table table-hover mb-0">
              <thead class="table-light">
                <tr>
                  <th>Trek</th>
                  <th>Date</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="booking in myBookings" :key="booking.booking_id">
                  <td>
                    <strong>{{ booking.trek_name }}</strong><br>
                    <small class="text-muted">{{ booking.location }}</small>
                  </td>
                  <td>{{ booking.booking_date }}</td>
                  <td>
                    <span class="badge"
                      :class="booking.status === 'Booked' ? 'bg-primary' : (booking.status === 'Completed' ? 'bg-success' : 'bg-danger')">
                      {{ booking.status }}
                    </span>
                  </td>
                  <td>
                    <button v-if="booking.status === 'Booked'" class="btn btn-sm btn-outline-danger"
                      @click="cancelBooking(booking.booking_id)">
                      Cancel
                    </button>
                  </td>
                </tr>
                <tr v-if="myBookings.length === 0">
                  <td colspan="4" class="text-center py-4">You haven't booked any treks yet.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      availableTreks: [],
      myBookings: [],
      searchQuery: '',
      filterDifficulty: '',
      message: '',
      isError: false
    }
  },
  mounted() {
    this.fetchOpenTreks()
    this.fetchMyBookings()
  },
  methods: {
    async fetchOpenTreks() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/user/treks', {
          params: { search: this.searchQuery, difficulty: this.filterDifficulty }
        })
        this.availableTreks = response.data
      } catch (err) {
        if (err.response?.status === 401) this.logout()
      }
    },
    async fetchMyBookings() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/user/bookings')
        this.myBookings = response.data
      } catch (err) {
        console.error("Error fetching bookings")
      }
    },
    async bookTrek(trekId) {
      this.message = ''
      try {
        const response = await axios.post(`http://127.0.0.1:5000/api/user/book/${trekId}`)
        this.isError = false
        this.message = response.data.message

        // Refresh both lists immediately
        this.fetchOpenTreks()
        this.fetchMyBookings()

        setTimeout(() => this.message = '', 4000)
      } catch (err) {
        this.isError = true
        this.message = err.response?.data?.message || 'Error booking trek.'
      }
    },
    async cancelBooking(bookingId) {
      if (!confirm('Are you sure you want to cancel this booking?')) return;

      try {
        const response = await axios.put(`http://127.0.0.1:5000/api/user/bookings/${bookingId}/cancel`);
        this.message = response.data.message;
        this.isError = false;

        // Refresh both lists to show updated slots and status
        this.fetchOpenTreks();
        this.fetchMyBookings();

        setTimeout(() => this.message = '', 3000);
      } catch (err) {
        this.isError = true;
        this.message = 'Error cancelling booking.';
      }
    },
    logout() {
      localStorage.removeItem('authToken')
      this.$router.push('/')
    }
  }
}
</script>