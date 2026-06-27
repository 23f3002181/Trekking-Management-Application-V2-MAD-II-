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
                  @click="toggleStatus(user.id)"
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
    
    <div class="alert alert-primary d-flex align-items-center" role="alert">
      <i class="bi bi-info-circle-fill me-2 fs-5"></i>
      <div>
        Blacklisted users cannot login or book treks.
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      userList: [],
      searchQuery: ''
    }
  },
  computed: {
    filteredUsers() {
      // If the search bar is empty, return everyone
      if (!this.searchQuery) return this.userList;
      
      const query = this.searchQuery.toLowerCase();
      
      // Filter the list based on name, email, or formatted ID
      return this.userList.filter(user => {
        const idString = `u${user.id.toString().padStart(3, '0')}`;
        return (
          (user.name && user.name.toLowerCase().includes(query)) ||
          (user.email && user.email.toLowerCase().includes(query)) ||
          idString.includes(query)
        );
      });
    }
  },
  mounted() {
    this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/admin/users')
        this.userList = response.data
      } catch (err) {
        console.error("Error fetching users:", err)
      }
    },
    async toggleStatus(userId) {
      try {
        await axios.put(`http://127.0.0.1:5000/api/admin/users/${userId}/toggle-status`)
        this.fetchUsers() // Refresh list to update UI
      } catch (err) {
        console.error("Error toggling user status:", err)
      }
    }
  }
}
</script>