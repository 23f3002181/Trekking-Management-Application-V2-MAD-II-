<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Staff Dashboard</h2>
      <button class="btn btn-outline-danger" @click="logout">Logout</button>
    </div>

    <div class="card shadow-sm mb-4">
      <div class="card-header bg-dark text-white">My Assigned Treks</div>
      <div class="card-body p-0">
        <table class="table table-hover mb-0 align-middle">
          <thead class="table-light">
            <tr>
              <th>Trek Name</th>
              <th>Location</th>
              <th>Available Slots</th>
              <th>Status</th>
              <th>Registered</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="trek in treks" :key="trek.id">
              <td><strong>{{ trek.name }}</strong><br><small class="text-muted">{{ trek.difficulty }}</small></td>
              <td>{{ trek.location }}</td>
              
              <td style="width: 150px;">
                <input type="number" class="form-control form-control-sm" v-model="trek.slots" min="0">
              </td>
              
              <td style="width: 180px;">
                <select class="form-select form-select-sm" v-model="trek.status">
                  <option value="Open">Open</option>
                  <option value="Closed">Closed</option>
                  <option value="Completed">Completed</option>
                </select>
              </td>
              
              <td><span class="badge bg-info text-dark">{{ trek.participants }} Trekkers</span></td>
              
              <td>
                <button class="btn btn-sm btn-success me-2" @click="updateTrek(trek)">Save</button>
                <button class="btn btn-sm btn-outline-primary" @click="viewParticipants(trek.id)">View List</button>
              </td>
            </tr>
            <tr v-if="treks.length === 0">
              <td colspan="6" class="text-center py-4">You have no assigned treks yet.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="message" class="alert alert-success mt-3">{{ message }}</div>

    <div v-if="selectedTrekId" class="card shadow-sm border-primary">
      <div class="card-header bg-primary text-white d-flex justify-content-between">
        <span>Participant List</span>
        <button class="btn btn-sm btn-close btn-close-white" @click="selectedTrekId = null"></button>
      </div>
      <div class="card-body p-0">
        <table class="table table-sm mb-0">
          <thead>
            <tr>
              <th>User Email</th>
              <th>Booking Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in participants" :key="user.booking_id">
              <td>{{ user.user_email }}</td>
              <td>{{ user.booking_date }}</td>
              <td><span class="badge bg-secondary">{{ user.status }}</span></td>
            </tr>
            <tr v-if="participants.length === 0">
              <td colspan="3" class="text-center py-2">No participants registered yet.</td>
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
      treks: [],
      participants: [],
      selectedTrekId: null,
      message: ''
    }
  },
  mounted() {
    this.fetchMyTreks()
  },
  methods: {
    async fetchMyTreks() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/staff/treks')
        this.treks = response.data
      } catch (err) {
        if (err.response?.status === 401) this.logout()
      }
    },
    async updateTrek(trek) {
      try {
        const response = await axios.put(`http://127.0.0.1:5000/api/staff/treks/${trek.id}`, {
          slots: trek.slots,
          status: trek.status
        })
        this.message = response.data.message
        setTimeout(() => this.message = '', 3000)
      } catch (err) {
        alert('Failed to update trek.')
      }
    },
    async viewParticipants(trekId) {
      try {
        this.selectedTrekId = trekId
        const response = await axios.get(`http://127.0.0.1:5000/api/staff/treks/${trekId}/participants`)
        this.participants = response.data
      } catch (err) {
        alert('Failed to load participants.')
      }
    },
    logout() {
      localStorage.removeItem('authToken')
      this.$router.push('/')
    }
  }
}
</script>