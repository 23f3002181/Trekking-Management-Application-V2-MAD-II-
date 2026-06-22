<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Admin Dashboard</h2>
      <button class="btn btn-outline-danger" @click="logout">Logout</button>
    </div>

    <div class="row mb-5">
      <div class="col-md-3">
        <div class="card text-white bg-primary mb-3 shadow-sm">
          <div class="card-body text-center">
            <h5 class="card-title">Total Treks</h5>
            <p class="card-text fs-2">{{ stats.total_treks }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-white bg-success mb-3 shadow-sm">
          <div class="card-body text-center">
            <h5 class="card-title">Total Trekkers</h5>
            <p class="card-text fs-2">{{ stats.total_users }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-white bg-warning mb-3 shadow-sm">
          <div class="card-body text-center">
            <h5 class="card-title">Trek Staff</h5>
            <p class="card-text fs-2">{{ stats.total_staff }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-white bg-danger mb-3 shadow-sm">
          <div class="card-body text-center">
            <h5 class="card-title">Total Bookings</h5>
            <p class="card-text fs-2">{{ stats.total_bookings }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="row mt-5">
      <div class="col-md-5">
        <div class="card shadow-sm mb-4">
          <div class="card-header bg-primary text-white">Create New Trek Route</div>
          <div class="card-body">
            <form @submit.prevent="createTrek">
              <div class="mb-3">
                <label>Trek Name</label>
                <input type="text" class="form-control" v-model="trekForm.name" required>
              </div>
              <div class="mb-3">
                <label>Location</label>
                <input type="text" class="form-control" v-model="trekForm.location" required>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label>Difficulty</label>
                  <select class="form-select" v-model="trekForm.difficulty" required>
                    <option value="Easy">Easy</option>
                    <option value="Moderate">Moderate</option>
                    <option value="Hard">Hard</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label>Duration (Days)</label>
                  <input type="number" class="form-control" v-model="trekForm.duration" min="1" required>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label>Available Slots</label>
                  <input type="number" class="form-control" v-model="trekForm.slots" min="1" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label>Assign Staff</label>
                  <select class="form-select" v-model="trekForm.staff_id">
                    <option value="">-- Unassigned --</option>
                    <option v-for="staff in staffList" :key="staff.id" :value="staff.id">
                      {{ staff.name }}
                    </option>
                  </select>
                </div>
              </div>
              <button type="submit" class="btn btn-primary w-100">Create Trek</button>
              <div v-if="trekMessage" class="alert alert-success mt-3 py-2">{{ trekMessage }}</div>
            </form>
          </div>
        </div>
      </div>

      <div class="col-md-7">
        <div class="card shadow-sm">
          <div class="card-header bg-secondary text-white">All Trek Routes</div>
          <div class="card-body p-0">
            <table class="table table-hover mb-0">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Location</th>
                  <th>Difficulty</th>
                  <th>Slots</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="trek in trekList" :key="trek.id">
                  <td>{{ trek.name }}</td>
                  <td>{{ trek.location }}</td>
                  <td>{{ trek.difficulty }}</td>
                  <td>{{ trek.slots }}</td>
                  <td>
                    <span class="badge" :class="trek.status === 'Open' ? 'bg-success' : 'bg-secondary'">
                      {{ trek.status }}
                    </span>
                  </td>
                </tr>
                <tr v-if="trekList.length === 0">
                  <td colspan="5" class="text-center py-3">No treks created yet.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <div class="card shadow-sm mb-4">
      <div class="card-header bg-dark text-white">Create New Trek Staff</div>
      <div class="card-body">
        <form @submit.prevent="createStaff" class="row g-3">
          <div class="col-md-6">
            <label>Full Name</label>
            <input type="text" class="form-control" v-model="staffForm.name" required>
          </div>
          <div class="col-md-6">
            <label>Contact Details</label>
            <input type="text" class="form-control" v-model="staffForm.contact" required>
          </div>
          <div class="col-md-6">
            <label>Email Address</label>
            <input type="email" class="form-control" v-model="staffForm.email" required>
          </div>
          <div class="col-md-6">
            <label>Temporary Password</label>
            <input type="password" class="form-control" v-model="staffForm.password" required>
          </div>
          <div class="col-12 mt-3">
            <button type="submit" class="btn btn-primary">Create Staff</button>
            <span class="ms-3 text-success" v-if="message">{{ message }}</span>
          </div>
        </form>
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
      staffForm: { name: '', contact: '', email: '', password: '' },
      message: '',
      
      // New Data for Treks
      trekForm: { name: '', location: '', difficulty: 'Moderate', duration: 1, slots: 10, staff_id: '' },
      trekList: [],
      staffList: [],
      trekMessage: ''
    }
  },
  mounted() {
    this.fetchStats()
    this.fetchTreksAndStaff()
  },
  methods: {
    async fetchStats() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/admin/stats')
        this.stats = response.data
      } catch (err) {
        if (err.response?.status === 401) this.logout()
      }
    },
    async fetchTreksAndStaff() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/admin/treks')
        this.trekList = response.data.treks
        this.staffList = response.data.staff
      } catch (err) {
        console.error("Error fetching treks", err)
      }
    },
    async createStaff() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/admin/staff', this.staffForm)
        this.message = response.data.message
        this.staffForm = { name: '', contact: '', email: '', password: '' }
        this.fetchStats()
        this.fetchTreksAndStaff() // Refresh staff dropdown
        setTimeout(() => this.message = '', 3000)
      } catch (err) {
        this.message = err.response?.data?.message || 'Error creating staff.'
      }
    },
    async createTrek() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/admin/treks', this.trekForm)
        this.trekMessage = response.data.message
        
        // Reset form to defaults
        this.trekForm = { name: '', location: '', difficulty: 'Moderate', duration: 1, slots: 10, staff_id: '' }
        
        // Refresh the lists to show the new trek
        this.fetchTreksAndStaff()
        this.fetchStats()
        
        setTimeout(() => this.trekMessage = '', 3000)
      } catch (err) {
        this.trekMessage = 'Error creating trek.'
      }
    },
    logout() {
      localStorage.removeItem('authToken')
      this.$router.push('/')
    }
  }
}
</script>