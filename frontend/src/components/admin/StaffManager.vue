<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Trekking Staff List</h2>
      <button class="btn btn-primary" @click="showForm = !showForm">
        {{ showForm ? 'Back to Staff List' : '+ Add New Staff' }}
      </button>
    </div>

    <div v-if="showForm" class="card shadow-sm border-0 mb-4">
      <div class="card-body">
        <form @submit.prevent="createStaff" class="row g-3">
          <div class="col-md-6">
            <label>Full Name</label>
            <input type="text" class="form-control" v-model="staffForm.name" required>
          </div>
          <div class="col-md-6">
            <label>Email Address</label>
            <input type="email" class="form-control" v-model="staffForm.email" required>
          </div>
          <div class="col-md-6">
            <label>Contact Number</label>
            <input type="text" class="form-control" v-model="staffForm.contact" required>
          </div>
          <div class="col-md-6">
            <label>Temporary Password</label>
            <input type="password" class="form-control" v-model="staffForm.password" required>
          </div>
          <div class="col-12 mt-4">
            <button type="submit" class="btn btn-primary px-4">Create Staff</button>
            <span class="ms-3 text-success" v-if="message">{{ message }}</span>
          </div>
        </form>
      </div>
    </div>

    <div v-else>
      <div class="mb-3 position-relative" style="max-width: 400px;">
        <i class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
        <input type="text" class="form-control ps-5" placeholder="Search staff by name or email..."
          v-model="searchQuery">
      </div>

      <div class="card shadow-sm border-0 mb-4">
        <div class="card-body p-0">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Contact</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="staff in filteredStaff" :key="staff.id">
                <td>TS{{ staff.id.toString().padStart(3, '0') }}</td>
                <td>{{ staff.name }}</td>
                <td>{{ staff.email }}</td>
                <td>{{ staff.contact }}</td>
                <td>
                  <span class="badge" :class="staff.active ? 'bg-success' : 'bg-danger'">
                    {{ staff.active ? 'Active' : 'Blacklisted' }}
                  </span>
                </td>
                <td>
                  <button class="btn btn-sm" :class="staff.active ? 'btn-outline-danger' : 'btn-outline-success'"
                    @click="toggleStatus(staff.user_id)">
                    {{ staff.active ? 'Blacklist' : 'Whitelist' }}
                  </button>
                </td>
              </tr>
              <tr v-if="filteredStaff.length === 0">
                <td colspan="6" class="text-center py-4">
                  {{ staffList.length === 0 ? 'No staff found in database.' : 'No staff match your search.' }}
                </td>
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

export default {
  data() {
    return {
      showForm: false,
      searchQuery: '',
      staffList: [],
      staffForm: { name: '', contact: '', email: '', password: '' },
      message: ''
    }
  },
  computed: {
    filteredStaff() {
      // If search is empty, show everyone
      if (!this.searchQuery) return this.staffList;

      const query = this.searchQuery.toLowerCase();

      // Filter by Name OR Email
      return this.staffList.filter(staff => {
        return (
          (staff.name && staff.name.toLowerCase().includes(query)) ||
          (staff.email && staff.email.toLowerCase().includes(query))
        );
      });
    }
  },
  mounted() {
    this.fetchStaff()
  },
  methods: {
    async fetchStaff() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/admin/staff')
        this.staffList = response.data
      } catch (err) {
        console.error("Error fetching staff:", err)
      }
    },
    async createStaff() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/admin/staff', this.staffForm)
        this.message = response.data.message
        this.staffForm = { name: '', contact: '', email: '', password: '' }
        this.fetchStaff()
        setTimeout(() => {
          this.message = ''
          this.showForm = false
        }, 2000)
      } catch (err) {
        this.message = err.response?.data?.message || 'Error creating staff.'
      }
    },
    async toggleStatus(userId) {
      try {
        await axios.put(`http://127.0.0.1:5000/api/admin/users/${userId}/toggle-status`)
        this.fetchStaff() // Refresh list to show new status
      } catch (err) {
        console.error("Error toggling status:", err)
      }
    }
  }
}
</script>