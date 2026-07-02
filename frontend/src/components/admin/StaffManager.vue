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
                    @click="toggleStatus(staff)">
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
import Swal from 'sweetalert2'

const Toast = Swal.mixin({
  toast: true, position: 'top-end', showConfirmButton: false, timer: 3000, timerProgressBar: true
})

export default {
  data() { 
    return { 
      showForm: false, 
      searchQuery: '', 
      staffList: [], 
      staffForm: { name: '', contact: '', email: '', password: '' }
    } 
  },
  computed: {
    filteredStaff() {
      if (!this.searchQuery) return this.staffList;
      const q = this.searchQuery.toLowerCase();
      return this.staffList.filter(s => s.name.toLowerCase().includes(q) || s.email.toLowerCase().includes(q));
    }
  },
  mounted() { this.fetchStaff() },
  methods: {
    async fetchStaff() {
      try {
        const token = localStorage.getItem('authToken')
        const res = await axios.get('http://127.0.0.1:5000/api/admin/staff', { 
          headers: { 'Authentication-Token': token } 
        })
        this.staffList = res.data
      } catch (err) {
        console.error(err)
      }
    },
    async createStaff() {
      try {
        const token = localStorage.getItem('authToken')
        const res = await axios.post('http://127.0.0.1:5000/api/admin/staff', this.staffForm, { 
          headers: { 'Authentication-Token': token } 
        })
        
        Toast.fire({ icon: 'success', title: res.data.message })
        
        this.staffForm = { name: '', contact: '', email: '', password: '' }
        this.fetchStaff()
        this.showForm = false
      } catch (err) { 
        Toast.fire({ icon: 'error', title: err.response?.data?.message || 'Failed to create staff.'})
      }
    },
    async toggleStatus(staff) {
      const actionText = staff.active ? 'Blacklist' : 'Whitelist'
      const actionColor = staff.active ? '#dc3545' : '#198754'

      const result = await Swal.fire({
        title: `Are you sure?`,
        text: `You are about to ${actionText.toLowerCase()} ${staff.name}.`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: actionColor,
        cancelButtonColor: '#6c757d',
        confirmButtonText: `Yes, ${actionText}!`
      })

      if (result.isConfirmed) {
        try {
          const token = localStorage.getItem('authToken')
          await axios.put(`http://127.0.0.1:5000/api/admin/users/${staff.user_id}/toggle-status`, {}, { 
            headers: { 'Authentication-Token': token } 
          })
          
          this.fetchStaff()
          Toast.fire({ icon: 'success', title: `Staff has been ${actionText.toLowerCase()}ed.` })
        } catch (err) {
          Toast.fire({ icon: 'error', title: 'Action failed.' })
        }
      }
    }
  }
}
</script>