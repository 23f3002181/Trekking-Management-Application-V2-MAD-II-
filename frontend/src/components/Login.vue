<template>
  <div class="d-flex align-items-center justify-content-center min-vh-100 bg-light py-5">
    <div class="container">
      <div class="row shadow-lg rounded-4 overflow-hidden" style="max-width: 950px; margin: auto; background: #ffffff;">
        
        <div class="col-md-5 p-5 d-flex flex-column justify-content-center position-relative text-white trek-sidebar">
          <div class="overlay"></div>
          
          <div class="position-relative z-1 h-100 d-flex flex-column">
            <div v-if="!isRegistering" class="mt-4">
              <h3 class="fw-bolder mb-3"><i class="bi bi-backpack4-fill text-success me-2"></i>TrekApp</h3>
              <p class="mb-5 opacity-75">Your gateway to the world's most breathtaking trails.</p>
              
              <ul class="list-unstyled mb-5 mt-4 custom-list">
                <li class="mb-4 d-flex align-items-center">
                  <div class="icon-box bg-white text-primary shadow-sm"><i class="bi bi-shield-lock-fill"></i></div>
                  <span class="fw-semibold ms-3">Admin Access</span>
                </li>
                <li class="mb-4 d-flex align-items-center">
                  <div class="icon-box bg-white text-success shadow-sm"><i class="bi bi-geo-alt-fill"></i></div>
                  <span class="fw-semibold ms-3">Trekking Staff</span>
                </li>
                <li class="mb-4 d-flex align-items-center">
                  <div class="icon-box bg-white text-info shadow-sm"><i class="bi bi-person-fill"></i></div>
                  <span class="fw-semibold ms-3">User (Trekker)</span>
                </li>
              </ul>
            </div>

            <div v-else class="text-center mt-5">
              <div class="display-1 mb-4">🏔️</div>
              <h3 class="fw-bolder mb-3">Join the Adventure</h3>
              <p class="opacity-75 small px-2">
                Create an account to browse, book, and manage your upcoming trekking experiences around the world.
              </p>
            </div>

            <div class="alert mt-auto mb-0 border-0 bg-dark bg-opacity-50 text-white backdrop-blur rounded-3" style="font-size: 0.8rem;">
              <i class="bi bi-info-circle-fill me-2 text-warning"></i>
              Only Users (Trekkers) can self-register. Staff accounts are managed by Admin.
            </div>
          </div>
        </div>

        <div class="col-md-7 p-5 d-flex flex-column justify-content-center bg-white">
          
          <div class="text-center mb-5">
            <h3 class="fw-bolder text-dark">{{ isRegistering ? 'Create Account' : 'Welcome Back' }}</h3>
            <p class="text-muted small">{{ isRegistering ? 'Fill in your details to get started' : 'Please enter your credentials to login' }}</p>
          </div>

          <form @submit.prevent="handleSubmit" novalidate>
            
            <div v-if="isRegistering" class="row mb-3">
              <div class="col-md-6 mb-3 mb-md-0">
                <label class="form-label text-muted small fw-bold mb-1">Full Name</label>
                <div class="input-group">
                  <span class="input-group-text bg-light border-end-0 text-muted"><i class="bi bi-person"></i></span>
                  <input type="text" class="form-control form-control-lg bg-light border-start-0 ps-0" 
                         :class="{'is-invalid': errors.fullName}" v-model="fullName" placeholder="John Doe">
                </div>
                <div class="text-danger small mt-1" v-if="errors.fullName">{{ errors.fullName }}</div>
              </div>
              <div class="col-md-6">
                <label class="form-label text-muted small fw-bold mb-1">Contact Number</label>
                <div class="input-group">
                  <span class="input-group-text bg-light border-end-0 text-muted"><i class="bi bi-telephone"></i></span>
                  <input type="tel" class="form-control form-control-lg bg-light border-start-0 ps-0" 
                         :class="{'is-invalid': errors.contactNumber}" v-model="contactNumber" placeholder="+91 9876543210">
                </div>
                <div class="text-danger small mt-1" v-if="errors.contactNumber">{{ errors.contactNumber }}</div>
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label text-muted small fw-bold mb-1">Email address</label>
              <div class="input-group">
                <span class="input-group-text bg-light border-end-0 text-muted"><i class="bi bi-envelope"></i></span>
                <input type="email" class="form-control form-control-lg bg-light border-start-0 ps-0" 
                       :class="{'is-invalid': errors.email}" v-model="email" placeholder="name@example.com">
              </div>
              <div class="text-danger small mt-1" v-if="errors.email">{{ errors.email }}</div>
            </div>

            <div :class="{'row': isRegistering, 'mb-2': true}">
              <div :class="{'col-md-6': isRegistering}">
                <label class="form-label text-muted small fw-bold mb-1">Password</label>
                <div class="input-group">
                  <span class="input-group-text bg-light border-end-0 text-muted"><i class="bi bi-lock"></i></span>
                  <input type="password" class="form-control form-control-lg bg-light border-start-0 ps-0" 
                         :class="{'is-invalid': errors.password}" v-model="password" placeholder="••••••••">
                </div>
                <div class="text-danger small mt-1" v-if="errors.password">{{ errors.password }}</div>
              </div>
              
              <div v-if="isRegistering" class="col-md-6 mt-3 mt-md-0">
                <label class="form-label text-muted small fw-bold mb-1">Confirm Password</label>
                <div class="input-group">
                  <span class="input-group-text bg-light border-end-0 text-muted"><i class="bi bi-shield-check"></i></span>
                  <input type="password" class="form-control form-control-lg bg-light border-start-0 ps-0" 
                         :class="{'is-invalid': errors.confirmPassword}" v-model="confirmPassword" placeholder="••••••••">
                </div>
                <div class="text-danger small mt-1" v-if="errors.confirmPassword">{{ errors.confirmPassword }}</div>
              </div>
            </div>
            
            <div v-if="!isRegistering" class="mb-4 d-flex justify-content-between align-items-center">
              <div class="form-check">
                <input type="checkbox" class="form-check-input" id="rememberMe">
                <label class="form-check-label small text-muted" for="rememberMe">Remember me</label>
              </div>
              <a href="#" class="text-decoration-none small text-primary fw-semibold">Forgot password?</a>
            </div>

            <button type="submit" class="btn btn-success btn-lg w-100 fw-bold mt-3 shadow-sm rounded-3" :disabled="isLoading">
              <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
              {{ isRegistering ? 'Create Account' : 'Login' }}
            </button>

            <div class="text-center mt-4 pt-2">
              <span class="text-muted small">
                {{ isRegistering ? 'Already have an account?' : "Don't have an account?" }}
              </span>
              <a href="#" @click.prevent="toggleMode" class="text-decoration-none text-primary fw-bold small ms-1 transition-all">
                {{ isRegistering ? 'Login here' : 'Register as Trekker' }}
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
import Swal from 'sweetalert2' 
import { useToast } from "vue-toastification"

export default {
  name: 'LoginRegisterScreen',
  setup() {
    const toast = useToast(); 
    return { toast };
  },
  data() {
    return {
      isRegistering: false,
      isLoading: false,
      fullName: '',
      contactNumber: '',
      email: '',
      password: '',
      confirmPassword: '',
      errors: {} 
    }
  },
  methods: {
    toggleMode() {
      this.isRegistering = !this.isRegistering
      this.fullName = ''
      this.contactNumber = ''
      this.email = ''
      this.password = ''
      this.confirmPassword = ''
      this.errors = {} 
    },

    validateForm() {
      this.errors = {};
      let isValid = true;

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!this.email) {
        this.errors.email = 'Email is required.';
        isValid = false;
      } else if (!emailRegex.test(this.email)) {
        this.errors.email = 'Please enter a valid email address.';
        isValid = false;
      }

      if (!this.password) {
        this.errors.password = 'Password is required.';
        isValid = false;
      } else if (this.password.length < 6) {
        this.errors.password = 'Password must be at least 6 characters.';
        isValid = false;
      }

      if (this.isRegistering) {
        if (!this.fullName || this.fullName.trim().length < 2) {
          this.errors.fullName = 'Please enter your full name.';
          isValid = false;
        }

        const phoneRegex = /^\+?[\d\s-]{8,15}$/;
        if (!this.contactNumber) {
          this.errors.contactNumber = 'Contact number is required.';
          isValid = false;
        } else if (!phoneRegex.test(this.contactNumber)) {
          this.errors.contactNumber = 'Please enter a valid phone number.';
          isValid = false;
        }
        if (this.password !== this.confirmPassword) {
          this.errors.confirmPassword = 'Passwords do not match.';
          isValid = false;
        }
      }

      return isValid;
    },

    async handleSubmit() {
      if (!this.validateForm()) {
        return; 
      }

      this.isLoading = true

      try {
        if (this.isRegistering) {
          await this.registerUser()
        } else {
          await this.loginUser()
        }
      } catch (err) {
        if (err.response && err.response.status === 403) {
          Swal.fire({
            title: 'Access Denied',
            text: err.response.data.message || 'Your account has been blacklisted.',
            icon: 'error',
            confirmButtonColor: '#dc3545',
            confirmButtonText: 'Understood'
          });
        } 
        else {
          this.toast.error(
            err.response?.data?.message || 
            (this.isRegistering ? 'Registration failed.' : 'Invalid email or password.')
          )
        }
      } finally {
        this.isLoading = false
      }
    },

    async registerUser() {
      const response = await axios.post('http://127.0.0.1:5000/api/register', {
        email: this.email,
        password: this.password,
        full_name: this.fullName,
        contact: this.contactNumber
      })
      
      this.toast.success(response.data.message || 'Registration successful! You can now login.')
      
      setTimeout(() => {
        this.isRegistering = false
        this.password = ''
        this.confirmPassword = ''
      }, 1500)
    },

    async loginUser() {
      const response = await axios.post('http://127.0.0.1:5000/api/login', {
        email: this.email,
        password: this.password
      })
      
      localStorage.setItem('authToken', response.data.token)
      localStorage.setItem('userRole', response.data.role)
      this.toast.success('Welcome back!')
      
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

.trek-sidebar {
  background-image: url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80');
  background-size: cover;
  background-position: center;
}

.overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.8) 0%, rgba(25, 135, 84, 0.6) 100%);
  z-index: 0;
}

.backdrop-blur {
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.icon-box {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.form-control-lg {
  font-size: 0.95rem;
}
.input-group-text, .form-control {
  border-color: #eaeaea;
}
.input-group-text {
  padding-left: 1rem;
}
.form-control:focus {
  box-shadow: none;
  background-color: #fff !important;
  border-color: #198754;
}
.input-group:focus-within .input-group-text,
.input-group:focus-within .form-control {
  background-color: #fff !important;
  border-color: #198754;
}
.input-group:focus-within .input-group-text i {
  color: #198754;
}

.is-invalid {
  border-color: #dc3545 !important;
  background-image: none !important; 
}
.input-group:has(.is-invalid) .input-group-text {
  border-color: #dc3545 !important;
  color: #dc3545 !important;
}

.transition-all {
  transition: all 0.2s ease;
}
.transition-all:hover {
  text-decoration: underline !important;
}
</style>