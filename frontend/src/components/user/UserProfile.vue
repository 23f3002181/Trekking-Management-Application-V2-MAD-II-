<template>
  <div class="container-fluid py-2">
    <h3 class="fw-bold mb-4">My Profile</h3>

    <div class="row">
      <div class="col-md-8 col-lg-6">
        <div class="card shadow-sm border-0">
          <div class="card-header bg-white border-bottom pb-0 pt-3">
            <h5 class="fw-bold text-primary">Personal Details</h5>
          </div>
          <div class="card-body p-4">
            <form @submit.prevent="updateProfile">
              
              <div class="mb-3">
                <label class="form-label fw-semibold">Full Name</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="profile.full_name" 
                  placeholder="e.g., Gautam Bhatt"
                  required
                >
              </div>

              <div class="mb-3">
                <label class="form-label fw-semibold">Email Address</label>
                <input 
                  type="email" 
                  class="form-control bg-light" 
                  v-model="profile.email" 
                  readonly
                >
                <div class="form-text">Email address cannot be changed.</div>
              </div>

              <div class="mb-4">
                <label class="form-label fw-semibold">Contact Number</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="profile.contact" 
                  placeholder="Enter your mobile number"
                >
              </div>

              <div class="d-grid">
                <button type="submit" class="btn btn-primary" :disabled="isSaving">
                  {{ isSaving ? 'Saving...' : 'Save Changes' }}
                </button>
              </div>

            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useToast } from "vue-toastification"

export default {
  setup() {
    const toast = useToast();
    return { toast };
  },
  data() {
    return {
      profile: {
        full_name: '',
        email: '',
        contact: ''
      },
      isSaving: false
    }
  },
  mounted() {
    this.fetchProfile()
  },
  methods: {
    async fetchProfile() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/user/profile')
        this.profile = res.data
      } catch (err) {
        this.toast.error('Failed to load profile data.')
      }
    },
    async updateProfile() {
      this.isSaving = true
      try {
        const res = await axios.put('http://127.0.0.1:5000/api/user/profile', {
          full_name: this.profile.full_name,
          contact: this.profile.contact
        })
        this.toast.success(res.data.message || "Profile updated successfully!")
        
      } catch (err) {
        this.toast.error('Failed to update profile.')
      } finally {
        this.isSaving = false
      }
    }
  }
}
</script>