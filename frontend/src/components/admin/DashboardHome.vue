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

    <h4 class="mb-3">Booking Management</h4>
    
    <div class="row mb-3">
      <div class="col-md-5">
        <div class="position-relative">
          <i class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
          <input 
            type="text" 
            class="form-control ps-5" 
            placeholder="Search by name, email, or trek..." 
            v-model="searchQuery"
          >
        </div>
      </div>
      <div class="col-md-3 offset-md-4">
        <select class="form-select" v-model="statusFilter">
          <option value="">All</option>
          <option value="Booked">Booked</option>
          <option value="Completed">Completed</option>
          <option value="Cancelled">Cancelled</option>
        </select>
      </div>
    </div>

    <div class="card shadow-sm border-0 mb-4">
      <div class="card-body p-0">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Trek Name</th>
              <th>Booking Date</th>
              <th>Start Date</th>
              <th>End Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="booking in paginatedBookings" :key="booking.id">
              <td>B{{ booking.id.toString().padStart(3, '0') }}</td>
              <td>{{ booking.user_name }}</td>
              <td>{{ booking.user_email }}</td>
              <td>{{ booking.trek_name }}</td>
              <td>{{ booking.booking_date }}</td>
              <td>{{ booking.start_date }}</td>
              <td>{{ booking.end_date }}</td>
              <td>
                <span class="badge" 
                      :class="{
                        'bg-primary': booking.status === 'Booked',
                        'bg-success': booking.status === 'Completed',
                        'bg-danger': booking.status === 'Cancelled'
                      }">
                  {{ booking.status }}
                </span>
              </td>
            </tr>
            <tr v-if="filteredBookings.length === 0">
              <td colspan="8" class="text-center py-4 text-muted">
                No bookings match your current filters.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div class="card-footer bg-white py-3 d-flex justify-content-between align-items-center" v-if="totalPages > 1">
        <span class="text-muted small">
          Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to 
          {{ Math.min(currentPage * itemsPerPage, filteredBookings.length) }} of {{ filteredBookings.length }} entries
        </span>
        
        <ul class="pagination pagination-sm mb-0">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button class="page-link text-dark" @click="currentPage--">Previous</button>
          </li>
          
          <li class="page-item" v-for="page in totalPages" :key="page" :class="{ active: currentPage === page }">
            <button class="page-link text-dark" @click="currentPage = page">{{ page }}</button>
          </li>
          
          <li class="page-item" :class="{ disabled: currentPage === totalPages }">
            <button class="page-link text-dark" @click="currentPage++">Next</button>
          </li>
        </ul>
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
      bookingList: [],
      
      // Filter & Pagination State
      searchQuery: '',
      statusFilter: '',
      currentPage: 1,
      itemsPerPage: 10 // Show 10 rows per page
    }
  },
  computed: {
    // 1. First, apply the Search and Status filters
    filteredBookings() {
      let result = this.bookingList;

      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase();
        result = result.filter(b => 
          (b.user_name && b.user_name.toLowerCase().includes(q)) ||
          (b.user_email && b.user_email.toLowerCase().includes(q)) ||
          (b.trek_name && b.trek_name.toLowerCase().includes(q))
        );
      }

      if (this.statusFilter) {
        result = result.filter(b => b.status === this.statusFilter);
      }

      return result;
    },
    // 2. Calculate the total number of pages needed for the filtered data
    totalPages() {
      return Math.ceil(this.filteredBookings.length / this.itemsPerPage) || 1;
    },
    // 3. Slice the data to only return the items for the current page
    paginatedBookings() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredBookings.slice(start, end);
    }
  },
  watch: {
    // Reset to page 1 automatically if the user changes the search or filter
    searchQuery() {
      this.currentPage = 1;
    },
    statusFilter() {
      this.currentPage = 1;
    }
  },
  mounted() {
    this.fetchStats()
    this.fetchAllBookings()
  },
  methods: {
    async fetchStats() {
      try {
        const token = localStorage.getItem('authToken')
        const response = await axios.get('http://127.0.0.1:5000/api/admin/stats', {
          headers: { 'Authentication-Token': token }
        })
        this.stats = response.data
      } catch (err) {
        console.error(err)
      }
    },
    async fetchAllBookings() {
      try {
        const token = localStorage.getItem('authToken')
        const response = await axios.get('http://127.0.0.1:5000/api/admin/bookings', {
          headers: { 'Authentication-Token': token }
        })
        this.bookingList = response.data
      } catch (err) {
        console.error("Error fetching bookings", err)
      }
    }
  }
}
</script>

<style scoped>
body, html {
  margin: 0;
  padding: 0;
  overflow: hidden; 
}
</style>