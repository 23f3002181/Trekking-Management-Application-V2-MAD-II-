<template>
  <div class="d-flex" style="height: 100vh;">
    <div class="bg-light border-end d-flex flex-column" style="width: 250px;">
      <router-link to="/" class="sidebar-heading p-3 border-bottom fw-bold d-flex align-items-center heading-link">
        <i class="bi bi-list fs-4 me-2"></i>
        Trekking Management
      </router-link>

      <div class="list-group list-group-flush mt-2">
        <router-link to="/admin-dashboard/home" class="list-group-item list-group-item-action bg-light border-0 py-3">
          <i class="bi bi-house-door me-3"></i> Dashboard
        </router-link>
        <router-link to="/admin-dashboard/treks" class="list-group-item list-group-item-action bg-light border-0 py-3">
          <i class="bi bi-geo-alt me-3"></i> Active Treks
        </router-link>
        <router-link to="/admin-dashboard/history" class="list-group-item list-group-item-action bg-light border-0 py-3">
          <i class="bi bi-clock-history me-3"></i> Trek History
        </router-link>
        <router-link to="/admin-dashboard/staff" class="list-group-item list-group-item-action bg-light border-0 py-3">
          <i class="bi bi-person-badge me-3"></i> Trekking Staff
        </router-link>
        <router-link to="/admin-dashboard/users"
          class="list-group-item list-group-item-action bg-light border-0 py-3 border-bottom">
          <i class="bi bi-people me-3"></i> Users (Trekkers)
        </router-link>

        <a href="#" @click.prevent="logout"
          class="list-group-item list-group-item-action bg-light border-0 py-3 text-danger fw-bold">
          <i class="bi bi-box-arrow-left me-3"></i> Logout
        </a>
      </div>
    </div>

    <div class="flex-grow-1 overflow-auto bg-white">
      <nav class="navbar navbar-expand-lg navbar-light border-bottom p-3 d-flex justify-content-end">
        <div class="dropdown">
          <button class="btn btn-light dropdown-toggle" type="button" data-bs-toggle="dropdown">
            <i class="bi bi-person-circle me-1"></i> Admin
          </button>
          <ul class="dropdown-menu dropdown-menu-end">
            <li><a class="dropdown-item" href="#" @click.prevent="logout">Logout</a></li>
          </ul>
        </div>
      </nav>
      <div class="p-4">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import Swal from 'sweetalert2'

export default {
  methods: {
    async logout() {
      const result = await Swal.fire({
        title: 'Are you sure?',
        text: "You will be logged out of your account.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545', 
        cancelButtonColor: '#6c757d',  
        confirmButtonText: 'Yes, log me out'
      })

      if (result.isConfirmed) {
        localStorage.removeItem('authToken')

        const Toast = Swal.mixin({
          toast: true, position: 'top-end', showConfirmButton: false, timer: 1500
        })
        Toast.fire({ icon: 'success', title: 'Logged out successfully' })

        this.$router.push('/')
      }
    }
  }
}
</script>

<style scoped>
.router-link-active {
  background-color: #e9ecef !important;
  color: #0d6efd !important;
  font-weight: 600;
  border-left: 4px solid #0d6efd !important;
}
.heading-link {
  text-decoration: none;
  color: inherit;
  cursor: pointer;
}

.heading-link:hover,
.heading-link:focus,
.heading-link:visited,
.heading-link:active {
  text-decoration: none;
  color: inherit;
}
</style>