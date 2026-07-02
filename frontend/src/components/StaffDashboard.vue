<template>
  <div class="d-flex" style="height: 100vh;">
    <div class="bg-light border-end d-flex flex-column" style="width: 250px;">
      <div class="sidebar-heading p-3 border-bottom fw-bold d-flex align-items-center">
        <i class="bi bi-list fs-4 me-2"></i> Trekking App
      </div>
      
      <div class="list-group list-group-flush mt-2">
        <router-link to="/staff-dashboard/home" class="list-group-item list-group-item-action bg-light border-0 py-3 border-bottom">
          <i class="bi bi-house-door me-3"></i> Dashboard
        </router-link>
        
        <a href="#" @click.prevent="logout" class="list-group-item list-group-item-action bg-light border-0 py-3 text-danger fw-bold">
          <i class="bi bi-box-arrow-left me-3"></i> Logout
        </a>
      </div>
    </div>

    <div class="flex-grow-1 overflow-auto bg-white">
      <nav class="navbar navbar-light border-bottom p-3 d-flex justify-content-end">
        <div class="fw-bold"><i class="bi bi-person-badge me-2"></i> Staff Member</div>
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
  name: 'StaffDashboard',
  methods: {
    async logout() {
      // 1. Fire the SweetAlert confirmation dialog
      const result = await Swal.fire({
        title: 'Ready to leave?',
        text: 'You will be logged out of your staff account.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545', // Danger red
        cancelButtonColor: '#6c757d', // Secondary gray
        confirmButtonText: 'Yes, log me out'
      });

      // 2. If the user clicks "Yes"
      if (result.isConfirmed) {
        localStorage.removeItem('authToken');
        
        // Optional: Show a quick toast before routing
        const Toast = Swal.mixin({
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 1500
        });
        Toast.fire({ icon: 'success', title: 'Logged out successfully' });

        // Redirect to the public home/login page
        this.$router.push('/');
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
</style>