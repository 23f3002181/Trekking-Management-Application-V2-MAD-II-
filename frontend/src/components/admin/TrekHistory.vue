<template>
  <div>
    <div v-if="!viewingParticipants">
      <h2 class="mb-4">Trek History (Completed)</h2>
      
      <div class="mb-3 position-relative" style="max-width: 400px;">
        <i class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
        <input type="text" class="form-control ps-5" placeholder="Search completed treks..." v-model="searchQuery">
      </div>

      <div class="card shadow-sm border-0">
        <div class="card-body p-0">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>ID</th>
                <th>Trek Name</th>
                <th>Difficulty</th>
                <th>Start Date</th> 
                <th>End Date</th>
                <th>Staff Led By</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="trek in filteredHistory" :key="trek.id">
                <td>{{ trek.id }}</td>
                <td><strong>{{ trek.name }}</strong><br><small class="text-muted">{{ trek.location }}</small></td>
                <td>{{ trek.difficulty }}</td>
                <td>{{ trek.start_date }}</td> 
                <td>{{ trek.end_date }}</td>
                <td>{{ trek.staff_name || 'N/A' }}</td>
                <td>
                  <button class="btn btn-sm btn-outline-primary" @click="viewParticipants(trek)">
                    <i class="bi bi-people"></i> View Participants
                  </button>
                </td>
              </tr>
              <tr v-if="filteredHistory.length === 0">
                <td colspan="5" class="text-center py-4 text-muted">No completed treks found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-else>
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Participants: <span class="text-primary">{{ selectedTrek.name }}</span></h2>
        <button class="btn btn-secondary" @click="viewingParticipants = false">
          &larr; Back to History
        </button>
      </div>

      <div class="card shadow-sm border-0">
        <div class="card-body p-0">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>Booking ID</th>
                <th>Trekker Name</th>
                <th>Email</th>
                <th>Contact</th>
                <th>Booking Date</th>
                <th>Booking Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in participants" :key="user.booking_id">
                <td>B{{ user.booking_id.toString().padStart(3, '0') }}</td>
                <td>{{ user.name }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.contact }}</td>
                <td>{{ user.booking_date }}</td>
                <td>
                  <span class="badge" 
                        :class="user.booking_status === 'Completed' ? 'bg-success' : (user.booking_status === 'Cancelled' ? 'bg-danger' : 'bg-primary')">
                    {{ user.booking_status }}
                  </span>
                </td>
              </tr>
              <tr v-if="participants.length === 0">
                <td colspan="6" class="text-center py-4 text-muted">No bookings found for this trek.</td>
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
import Swal from 'sweetalert2'

export default {
  data() {
    return {
      searchQuery: '',
      trekList: [],
      viewingParticipants: false,
      selectedTrek: null,
      participants: []
    }
  },
  computed: {
    filteredHistory() {
      let historyTreks = this.trekList.filter(t => t.status === 'Completed');
      
      if (!this.searchQuery) return historyTreks;
      
      const q = this.searchQuery.toLowerCase();
      return historyTreks.filter(t => t.name.toLowerCase().includes(q) || t.location.toLowerCase().includes(q));
    }
  },
  mounted() {
    this.fetchTreks()
  },
  methods: {
    async fetchTreks() {
      try {
        const token = localStorage.getItem('authToken')
        const res = await axios.get('http://127.0.0.1:5000/api/admin/treks', {
          headers: { 'Authentication-Token': token }
        })
        this.trekList = res.data.treks
      } catch (err) {
        console.error("Error fetching treks for history", err)
      }
    },
    async viewParticipants(trek) {
      this.selectedTrek = trek;
      try {
        const token = localStorage.getItem('authToken')
        const res = await axios.get(`http://127.0.0.1:5000/api/admin/treks/${trek.id}/participants`, {
          headers: { 'Authentication-Token': token }
        })
        this.participants = res.data;
        this.viewingParticipants = true; 
      } catch (err) {
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Failed to load participants.'
        })
      }
    }
  }
}
</script>