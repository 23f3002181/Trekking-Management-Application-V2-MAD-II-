<template>
  <div>
    <h2 class="mb-4">Dashboard</h2>
    
    <div class="row mb-5">
      <div class="col-md-3">
        <div class="card bg-white border shadow-sm">
          <div class="card-body text-center">
            <h6 class="text-muted">Total Treks</h6>
            <h2 class="mb-0">{{ stats.total_treks }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-white border shadow-sm">
          <div class="card-body text-center">
            <h6 class="text-muted">Total Users (Trekkers)</h6>
            <h2 class="mb-0">{{ stats.total_users }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-white border shadow-sm">
          <div class="card-body text-center">
            <h6 class="text-muted">Total Trekking Staff</h6>
            <h2 class="mb-0">{{ stats.total_staff }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-white border shadow-sm">
          <div class="card-body text-center">
            <h6 class="text-muted">Total Bookings</h6>
            <h2 class="mb-0">{{ stats.total_bookings }}</h2>
          </div>
        </div>
      </div>
    </div>

    <h4 class="mb-3">Recent Bookings</h4>
    <div class="card shadow-sm border-0">
      <div class="card-body p-0">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th>Booking ID</th>
              <th>User Email</th>
              <th>Trek Name</th>
              <th>Booking Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="booking in bookingList" :key="booking.id">
              <td>{{ booking.id }}</td>
              <td>{{ booking.user_email }}</td>
              <td>{{ booking.trek_name }}</td>
              <td>{{ booking.date }}</td>
              <td>
                <span class="badge" :class="booking.status === 'Booked' ? 'bg-primary' : 'bg-secondary'">
                  {{ booking.status }}
                </span>
              </td>
            </tr>
            <tr v-if="bookingList.length === 0">
              <td colspan="5" class="text-center py-4">No bookings found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      stats: { total_treks: 0, total_users: 0, total_staff: 0, total_bookings: 0 },
      bookingList: []
    }
  },
  mounted() {
    this.fetchStats()
    this.fetchAllBookings()
  },
  methods: {
    async fetchStats() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/admin/stats')
        this.stats = response.data
      } catch (err) {
        console.error(err)
      }
    },
    async fetchAllBookings() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/admin/bookings')
        this.bookingList = response.data
      } catch (err) {
        console.error("Error fetching bookings", err)
      }
    }
  }
}
</script>