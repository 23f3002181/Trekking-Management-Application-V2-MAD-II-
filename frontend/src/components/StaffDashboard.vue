<template>
  <div class="d-flex" style="height: 100vh;">
    <div class="bg-light border-end d-flex flex-column" style="width: 250px;">
      <div class="p-3 text-center border-bottom">
        <router-link to="/">
          <span class="glyphicon glyphicon-th-list"><i class="bi bi-list"></i></span>
        </router-link>
      </div>

      <div class="list-group list-group-flush mt-2">
        <router-link to="/staff-dashboard/home"
          class="list-group-item list-group-item-action bg-light border-0 py-3 border-bottom">
          <i class="bi bi-house-door me-3"></i> Dashboard
        </router-link>

        <a href="#" @click.prevent="logout"
          class="list-group-item list-group-item-action bg-light border-0 py-3 text-danger fw-bold">
          <i class="bi bi-box-arrow-left me-3"></i> Logout
        </a>
      </div>
    </div>
    <div class="flex-grow-1 d-flex flex-column">
      <div class="bg-light border-bottom px-4 py-2 d-flex justify-content-between align-items-center">
        <h4 class="fw-bold mb-0 py-0 fs-3 text-black">
          Trekking Management Application
        </h4>
        <nav class="navbar navbar-light border-bottom d-flex justify-content-end">
          <div class="fw-bold"><i class="bi bi-person-badge me-2"></i> Staff Member</div>
        </nav>
      </div>
      <div class="p-5 bg-white flex-grow-1 overflow-auto">
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
      const result = await Swal.fire({
        title: 'Ready to leave?',
        text: 'You will be logged out of your staff account.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545', 
        cancelButtonColor: '#6c757d', 
        confirmButtonText: 'Yes, log me out'
      });

      if (result.isConfirmed) {
        localStorage.removeItem('authToken');
        const Toast = Swal.mixin({
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          timer: 1500
        });
        Toast.fire({ icon: 'success', title: 'Logged out successfully' });
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