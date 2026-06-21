<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-body">
            <h3 class="card-title text-center mb-4">
              {{ isRegistering ? 'Trekker Registration' : 'Login' }}
            </h3>

            <form @submit.prevent="handleSubmit">
              <div class="mb-3">
                <label class="form-label">Email address</label>
                <input type="email" class="form-control" v-model="email" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Password</label>
                <input type="password" class="form-control" v-model="password" required>
              </div>
              
              <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary">
                  {{ isRegistering ? 'Register' : 'Login' }}
                </button>
              </div>
            </form>

            <div v-if="message" class="alert mt-3" :class="isError ? 'alert-danger' : 'alert-success'">
              {{ message }}
            </div>

            <div class="text-center mt-3">
              <a href="#" @click.prevent="toggleMode" class="text-decoration-none">
                {{ isRegistering ? 'Already have an account? Login here' : 'New Trekker? Register here' }}
              </a>
            </div>
            
          </div>
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
      isRegistering: false,
      email: '',
      password: '',
      message: '',
      isError: false
    }
  },
  methods: {
    toggleMode() {
      this.isRegistering = !this.isRegistering
      this.message = ''
      this.email = ''
      this.password = ''
    },
    async handleSubmit() {
      if (this.isRegistering) {
        await this.registerUser()
      } else {
        await this.loginUser()
      }
    },
    async registerUser() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/register', {
          email: this.email,
          password: this.password
        })
        this.isError = false
        this.message = response.data.message + '. You can now login.'
        this.isRegistering = false // Switch back to login view
        this.password = '' // Clear password for safety
      } catch (err) {
        this.isError = true
        this.message = err.response?.data?.message || 'Registration failed.'
      }
    },
    async loginUser() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/login', {
          email: this.email,
          password: this.password
        })
        
        // Save the token
        localStorage.setItem('authToken', response.data.token)
        
        // RBAC Redirection
        const role = response.data.role
        if (role === 'admin') {
          this.$router.push('/admin-dashboard')
        } else if (role === 'staff') {
          this.$router.push('/staff-dashboard')
        } else {
          this.$router.push('/user-dashboard')
        }
      } catch (err) {
        this.isError = true
        this.message = 'Invalid email or password.'
      }
    }
  }
}
</script>