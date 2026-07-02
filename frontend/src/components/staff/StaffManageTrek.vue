<template>
  <div v-if="trek">
    <div class="mb-4">
      <router-link to="/staff-dashboard/home" class="text-decoration-none d-flex align-items-center">
        <i class="bi bi-arrow-left me-2"></i> Back to My Treks
      </router-link>
    </div>

    <h2 class="mb-4">Trek Details: {{ trek.name }}</h2>

    <div class="row">
      <div class="col-md-4 mb-4">
        <div class="p-3 bg-light rounded border mb-4">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <label class="fw-bold mb-0 text-secondary">Capacity Management</label>
            <span class="badge bg-primary rounded-pill">
              {{ trek.total_slots - trek.available_slots }} Booked
            </span>
          </div>

          <div class="mb-3">
            <label class="form-label small text-muted mb-1">Update Total Slots</label>
            <div class="input-group input-group-sm">
              <input type="number" class="form-control" v-model="trek.total_slots" min="1"
                :disabled="trek.status === 'Completed'">
              <span class="input-group-text bg-white">Slots</span>
            </div>
          </div>

          <div class="mb-1 d-flex justify-content-between small">
            <span class="text-muted">Available</span>
            <strong :class="trek.available_slots <= 0 ? 'text-danger' : 'text-success'">
              {{ trek.available_slots }} / {{ trek.total_slots }}
            </strong>
          </div>
          <div class="progress" style="height: 8px;">
            <div class="progress-bar" :class="trek.available_slots <= 0 ? 'bg-danger' : 'bg-success'" role="progressbar"
              :style="{ width: ((trek.total_slots - trek.available_slots) / (trek.total_slots || 1) * 100) + '%' }">
            </div>
          </div>
        </div>

        <div class="card shadow-sm border-0">
          <div class="card-body">
            <h5 class="card-title border-bottom pb-2 mb-3">Settings</h5>

            <p class="mb-1"><strong>Difficulty:</strong> {{ trek.difficulty }}</p>
            <p class="mb-3"><strong>Duration:</strong> {{ trek.duration }} Days</p>

            <div class="mb-3 row">
              <div class="col-6">
                <label class="fw-bold mb-1 small text-muted">Start Date</label>
                <input type="date" class="form-control form-control-sm" v-model="trek.start_date"
                  :disabled="trek.status === 'Started' || trek.status === 'Completed'">
              </div>
              <div class="col-6">
                <label class="fw-bold mb-1 small text-muted">End Date</label>
                <input type="date" class="form-control form-control-sm" v-model="trek.end_date"
                  :disabled="trek.status === 'Completed'">
              </div>
            </div>

            <div class="mb-3">
              <label class="fw-bold mb-2 small text-muted">Status</label>
              <select class="form-select" v-model="trek.status"
                :disabled="trek.status === 'Started' || trek.status === 'Completed'">
                <option value="Open">Open</option>
                <option value="Closed">Closed</option>
                <option value="Started" disabled>Started</option>
                <option value="Completed" disabled>Completed</option>
              </select>
            </div>

            <div class="d-grid gap-2 mt-4">
              <button class="btn btn-primary" @click="updateTrek(trek.status)" :disabled="trek.status === 'Completed'">
                {{ trek.status === 'Completed' ? 'Trek Finalized' : 'Save Changes' }}
              </button>

              <button class="btn btn-warning text-dark fw-bold" @click="markAsStarted"
                v-if="trek.status === 'Open' || trek.status === 'Closed'">
                <i class="bi bi-play-circle me-1"></i> Mark as Started
              </button>

              <button class="btn btn-success fw-bold" @click="updateTrek('Completed')" v-if="trek.status === 'Started'">
                <i class="bi bi-check2-all me-1"></i> Mark as Completed
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-8">

        <div v-if="trek.status !== 'Completed'">
          <div class="d-flex justify-content-between align-items-end mb-3">
            <h5 class="mb-0">Active Participants ({{ activeParticipants.length }})</h5>
          </div>
          <div class="card shadow-sm border-0">
            <div class="card-body p-0">
              <table class="table table-hover mb-0 align-middle">
                <thead class="table-light">
                  <tr>
                    <th class="ps-3">#</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Booking Date</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="p in activeParticipants" :key="p.booking_id">
                    <td class="ps-3 text-muted">{{ p.index }}</td>
                    <td><strong>{{ p.user_name }}</strong></td>
                    <td>{{ p.user_email }}</td>
                    <td>{{ p.booking_date }}</td>
                    <td>
                      <span class="badge bg-primary">{{ p.status }}</span>
                    </td>
                  </tr>
                  <tr v-if="activeParticipants.length === 0">
                    <td colspan="5" class="text-center py-4 text-muted">No active participants found.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div v-else>
          <StaffCompletedBookings :trek-id="trek.id" />
        </div>

      </div>
    </div>
  </div>

  <div v-else class="text-center py-5">
    <div class="spinner-border text-primary" role="status"></div>
  </div>
</template>

<script>
import axios from 'axios'
import { useToast } from "vue-toastification"
import Swal from 'sweetalert2'
import StaffCompletedBookings from './StaffCompletedBookings.vue'

export default {
  components: {
    StaffCompletedBookings
  },
  setup() {
    const toast = useToast();
    return { toast };
  },
  data() {
    return {
      trek: null,
      participants: []
    }
  },
  computed: {
    // Keeps the active table clean by hiding users who are already completed
    activeParticipants() {
      return this.participants.filter(p => p.status !== 'Completed')
    }
  },
  mounted() {
    this.fetchTrekDetails()
    this.fetchParticipants()
  },
  methods: {
    async fetchTrekDetails() {
      try {
        const token = localStorage.getItem('authToken')
        const trekId = this.$route.params.id
        const res = await axios.get(`http://127.0.0.1:5000/api/staff/treks/${trekId}`, {
          headers: { 'Authentication-Token': token }
        })
        this.trek = res.data
      } catch (err) {
        this.toast.error("Error fetching trek details.")
      }
    },

    async fetchParticipants() {
      try {
        const token = localStorage.getItem('authToken')
        const trekId = this.$route.params.id
        const res = await axios.get(`http://127.0.0.1:5000/api/staff/treks/${trekId}/participants`, {
          headers: { 'Authentication-Token': token }
        })
        this.participants = res.data
      } catch (err) {
        this.toast.error("Error fetching participants.")
      }
    },

    // Helper to get today's date in YYYY-MM-DD format for HTML date inputs
    getTodayDate() {
      const today = new Date();
      return today.toISOString().split('T')[0];
    },

    // 1. The linear workflow method to start the trek
    async markAsStarted() {
      // Fire the SweetAlert confirmation
      const result = await Swal.fire({
        title: 'Start this Trek?',
        text: "This will officially begin the trek and lock the start date. Are you sure?",
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#ffc107', // Bootstrap Warning Yellow to match your HTML button
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Yes, start it!'
      });

      // Stop execution if they click "Cancel"
      if (!result.isConfirmed) return;

      // Automatically assign today's date to the start date
      this.trek.start_date = this.getTodayDate();

      // Proceed with the database update
      await this.updateTrek('Started');
    },

    // 2. The Core Update Method
    async updateTrek(newStatus) {
      // Intercept the "Completed" status with a SweetAlert warning
      if (newStatus === 'Completed') {
        const result = await Swal.fire({
          title: 'Mark Trek as Completed?',
          text: "This will also mark all active bookings as completed. You cannot undo this!",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#198754',
          cancelButtonColor: '#6c757d',
          confirmButtonText: 'Yes, complete it!'
        });

        // Stop execution if they click "Cancel"
        if (!result.isConfirmed) return;

        // Automatically assign today's date to the end date
        this.trek.end_date = this.getTodayDate();
      }

      // Execute the API update
      try {
        const token = localStorage.getItem('authToken')
        const trekId = this.$route.params.id

        // Build payload including dynamic slots and dates
        const payload = {
          status: newStatus,
          total_slots: this.trek.total_slots,
          start_date: this.trek.start_date,
          end_date: this.trek.end_date
        };

        const res = await axios.put(`http://127.0.0.1:5000/api/staff/treks/${trekId}`, payload, {
          headers: { 'Authentication-Token': token }
        })

        // Update UI state and fire success toast
        this.toast.success(`Saved changes successfully! Trek is now ${newStatus}.`)
        this.trek.status = newStatus

        // Update available slots dynamically from backend calculation
        if (res.data.available_slots !== undefined) {
          this.trek.available_slots = res.data.available_slots;
        }

        // Refresh the participant list to reflect the backend cascade effect immediately
        if (newStatus === 'Completed') {
          this.fetchParticipants()
        }

      } catch (err) {
        this.toast.error('Failed to update trek.')
      }
    }
  }
}
</script>