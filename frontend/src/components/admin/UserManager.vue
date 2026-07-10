<template>
  <div>
    <h2 class="mb-4">Users (Trekkers)</h2>

    <div class="mb-3 position-relative" style="max-width: 400px;">
      <i class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
      <input 
        type="text" 
        class="form-control ps-5" 
        placeholder="Search users by name, email, or ID..."
        v-model="searchQuery"
      >
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
            <tr v-for="user in filteredUsers" :key="user.id">
              <td>U{{ user.id.toString().padStart(3, '0') }}</td>
              <td>{{ user.name }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.contact }}</td>
              <td>
                <span class="badge" :class="user.active ? 'bg-success border border-success text-success bg-opacity-10' : 'bg-danger border border-danger text-danger bg-opacity-10'">
                  {{ user.active ? 'Active' : 'Blacklisted' }}
                </span>
              </td>
              <td>
                <button 
                  class="btn btn-sm" 
                  :class="user.active ? 'btn-outline-danger' : 'btn-outline-success'"
                  @click="toggleStatus(user)"
                >
                  {{ user.active ? 'Blacklist' : 'Whitelist' }}
                </button>
              </td>
            </tr>
            <tr v-if="userList.length === 0">
              <td colspan="6" class="text-center py-4 text-muted">
                No users found.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div class="alert alert-primary d-inline-flex align-items-center" role="alert">
      <i class="bi bi-info-circle-fill me-2 fs-5"></i>
      <div>
        Blacklisted users cannot login.
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
  data() { return { userList: [], searchQuery: '' } },
  computed: {
    filteredUsers() {
      if (!this.searchQuery) return this.userList;
      const q = this.searchQuery.toLowerCase();
      return this.userList.filter(u => (u.name && u.name.toLowerCase().includes(q)) || (u.email && u.email.toLowerCase().includes(q)));
    }
  },
  mounted() { this.fetchUsers() },
  methods: {
    async fetchUsers() {
      try {
        const token = localStorage.getItem('authToken')
        const res = await axios.get('http://127.0.0.1:5000/api/admin/users', { 
          headers: { 'Authentication-Token': token } 
        })
        this.userList = res.data
      } catch (err) {
        console.error(err)
      }
    },
    async toggleStatus(user) {
      const actionText = user.active ? 'Blacklist' : 'Whitelist'
      const actionColor = user.active ? '#dc3545' : '#198754'

      const result = await Swal.fire({
        title: `Are you sure?`,
        text: `You are about to ${actionText.toLowerCase()} ${user.name}.`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: actionColor,
        cancelButtonColor: '#6c757d',
        confirmButtonText: `Yes, ${actionText}!`
      })

      if (result.isConfirmed) {
        try {
          const token = localStorage.getItem('authToken')
          await axios.put(`http://127.0.0.1:5000/api/admin/users/${user.id}/toggle-status`, {}, { 
            headers: { 'Authentication-Token': token } 
          })
          
          this.fetchUsers()
          Toast.fire({ icon: 'success', title: `User has been ${actionText.toLowerCase()}ed.` })
        } catch (err) {
          Toast.fire({ icon: 'error', title: 'Action failed.' })
        }
      }
    }
  }
}
</script>