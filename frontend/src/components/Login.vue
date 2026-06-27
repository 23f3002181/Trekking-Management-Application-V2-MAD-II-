<template>
  <div class="d-flex align-items-center justify-content-center min-vh-100 bg-light py-5">
    <div class="container">
      <div class="row bg-white shadow-lg rounded-4 overflow-hidden" style="max-width: 950px; margin: auto;">
        
        <div class="col-md-5 p-5 bg-light border-end d-flex flex-column justify-content-center position-relative">
          
          <div v-if="!isRegistering">
            <h4 class="fw-bold mb-4">🏔️ Trekking Management Application</h4>
            <p class="text-muted mb-4 small">Select your role to access the system.</p>
            
            <ul class="list-unstyled mb-5 mt-4">
              <li class="mb-3 d-flex align-items-center">
                <i class="bi bi-shield-lock fs-4 me-3 text-primary"></i>
                <span class="fw-semibold text-secondary">Admin</span>
              </li>
              <li class="mb-3 d-flex align-items-center">
                <i class="bi bi-person-badge fs-4 me-3 text-success"></i>
                <span class="fw-semibold text-secondary">Trekking Staff</span>
              </li>
              <li class="mb-3 d-flex align-items-center">
                <i class="bi bi-person fs-4 me-3 text-info"></i>
                <span class="fw-semibold text-secondary">User (Trekker)</span>
              </li>
            </ul>
          </div>

          <div v-else class="text-center">
            <h1 class="display-1 mb-3">🧗</h1>
            <h4 class="fw-bold mb-3">Join the Adventure</h4>
            <p class="text-muted small">
              Create an account to browse, book, and manage your upcoming trekking experiences around the world.
            </p>
          </div>

          <div class="alert alert-primary py-2 mt-auto mb-0 border-0 bg-primary bg-opacity-10" style="font-size: 0.8rem;">
            <i class="bi bi-info-circle me-1"></i>
            <strong>Note:</strong> Only Users (Trekkers) can register themselves. Trekking Staff are created by Admin.
          </div>
        </div>


        <div class="col-md-7 p-5 d-flex flex-column justify-content-center">
          
          <div class="text-center mb-4">
            <h3 class="fw-bold">{{ isRegistering ? 'Create User Account' : 'Welcome Back!' }}</h3>
            <p class="text-muted">{{ isRegistering ? 'Register as a Trekker' : 'Login to your account' }}</p>
          </div>

          <form @submit.prevent="handleSubmit">
            
            <div v-if="isRegistering" class="row mb-3">
              <div class="col-md-6 mb-3 mb-md-0">
                <label class="form-label text-muted small fw-bold">Full Name</label>
                <div class="input-group">
                  <span class="input-group-text bg-white"><i class="bi bi-person"></i></span>
                  <input type="text" class="form-control border-start-0 ps-0" v-model="fullName" placeholder="John Doe" required>
                </div>
              </div>
              <div class="col-md-6">
                <label class="form-label text-muted small fw-bold">Contact Number</label>
                <div class="input-group">
                  <span class="input-group-text bg-white"><i class="bi bi-telephone"></i></span>
                  <input type="tel" class="form-control border-start-0 ps-0" v-model="contactNumber" placeholder="+91 9876543210" required>
                </div>
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label text-muted small fw-bold">Email address</label>
              <div class="input-group">
                <span class="input-group-text bg-white"><i class="bi bi-envelope"></i></span>
                <input type="email" class="form-control border-start-0 ps-0" v-model="email" placeholder="Enter email address" required>
              </div>
            </div>

            <div :class="{'row': isRegistering, 'mb-3': true}">
              <div :class="{'col-md-6': isRegistering}">
                <label class="form-label text-muted small fw-bold">Password</label>
                <div class="input-group">
                  <span class="input-group-text bg-white"><i class="bi bi-lock"></i></span>
                  <input type="password" class="form-control border-start-0 ps-0" v-model="password" placeholder="Enter password" required>
                </div>
              </div>
              
              <div v-if="isRegistering" class="col-md-6 mt-3 mt-md-0">
                <label class="form-label text-muted small fw-bold">Confirm Password</label>
                <div class="input-group">
                  <span class="input-group-text bg-white"><i class="bi bi-shield-lock"></i></span>
                  <input type="password" class="form-control border-start-0 ps-0" v-model="confirmPassword" placeholder="Confirm password" required>
                </div>
              </div>
            </div>
            
            <div v-if="!isRegistering" class="mb-4 form-check">
              <input type="checkbox" class="form-check-input" id="rememberMe">
              <label class="form-check-label small text-muted" for="rememberMe">Remember me</label>
            </div>

            <div v-if="message" class="alert py-2 small d-flex align-items-center" :class="isError ? 'alert-danger' : 'alert-success'">
              <i class="bi me-2" :class="isError ? 'bi-exclamation-triangle-fill' : 'bi-check-circle-fill'"></i>
              {{ message }}
            </div>

            <button type="submit" class="btn btn-primary w-100 py-2 fw-bold mt-2" :disabled="isLoading">
              <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
              {{ isRegistering ? 'Register' : 'Login' }}
            </button>

            <div class="text-center mt-4 border-top pt-3">
              <span class="text-muted small">
                {{ isRegistering ? 'Already have an account?' : "Don't have an account?" }}
              </span>
              <a href="#" @click.prevent="toggleMode" class="text-decoration-none fw-bold small ms-1">
                {{ isRegistering ? 'Login here' : 'Register as User (Trekker)' }}
              </a>
            </div>

          </form>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LoginRegisterScreen',
  data() {
    return {
      isRegistering: false,
      isLoading: false,
      // Form Fields
      fullName: '',
      contactNumber: '',
      email: '',
      password: '',
      confirmPassword: '',
      // Feedback
      message: '',
      isError: false
    }
  },
  methods: {
    toggleMode() {
      this.isRegistering = !this.isRegistering
      this.message = ''
      this.isError = false
      // Clear all fields on toggle
      this.fullName = ''
      this.contactNumber = ''
      this.email = ''
      this.password = ''
      this.confirmPassword = ''
    },
    async handleSubmit() {
      this.message = ''
      this.isError = false
      this.isLoading = true

      try {
        if (this.isRegistering) {
          // Frontend Validation: Check if passwords match
          if (this.password !== this.confirmPassword) {
            this.isError = true
            this.message = 'Passwords do not match!'
            this.isLoading = false
            return
          }
          await this.registerUser()
        } else {
          await this.loginUser()
        }
      } catch (err) {
        this.isError = true
        // Keep your original error handling style
        this.message = err.response?.data?.message || (this.isRegistering ? 'Registration failed.' : 'Invalid email or password.')
      } finally {
        this.isLoading = false
      }
    },
    async registerUser() {
      // Kept your exact API endpoint. 
      // Note: Added fullName and contactNumber to the payload just in case you update your backend to save them!
      const response = await axios.post('http://127.0.0.1:5000/api/register', {
        email: this.email,
        password: this.password,
        full_name: this.fullName,
        contact: this.contactNumber
      })
      this.isError = false
      this.message = response.data.message + ' You can now login.'
      
      // Auto-switch to login mode after successful registration
      setTimeout(() => {
        this.isRegistering = false
        this.password = ''
        this.confirmPassword = ''
      }, 1500)
    },
    async loginUser() {
      // Kept your exact API endpoint and routing logic!
      const response = await axios.post('http://127.0.0.1:5000/api/login', {
        email: this.email,
        password: this.password
      })
      
      localStorage.setItem('authToken', response.data.token)
      
      const role = response.data.role
      if (role === 'admin') {
        this.$router.push('/admin-dashboard')
      } else if (role === 'staff') {
        this.$router.push('/staff-dashboard')
      } else {
        this.$router.push('/user-dashboard')
      }
    }
  }
}
</script>

<style scoped>
/* Optional slight shadow for the inputs to match wireframe depth */
.input-group-text, .form-control {
  box-shadow: none !important;
  border-color: #dee2e6;
}
.form-control:focus {
  border-color: #0d6efd;
}
</style>