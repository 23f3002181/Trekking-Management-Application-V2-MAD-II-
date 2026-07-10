<template>
  <div>
    <div class="d-flex justify-content-between align-items-end mb-3">
      <h5 class="mb-0 text-success">
        <i class="bi bi-clock-history me-2"></i>Completed Participants ({{ completedParticipants.length }})
      </h5>
    </div>
    
    <div class="card shadow-sm border-0 border-success border-start border-4">
      <div class="card-body p-0">
        <table class="table table-hover mb-0 align-middle">
          <thead class="table-light">
            <tr>
              <th class="ps-4">S.No.</th>
              <th>Name</th>
              <th>Email</th>
              <th>Booking Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(p, index) in completedParticipants" :key="p.booking_id">
              <td class="ps-4 text-muted">{{ index + 1 }}</td>
              <td><strong>{{ p.user_name }}</strong></td>
              <td>{{ p.user_email }}</td>
              <td>{{ p.booking_date }}</td>
              <td>
                <span class="badge bg-success">Completed</span>
              </td>
            </tr>
            <tr v-if="completedParticipants.length === 0">
              <td colspan="5" class="text-center py-4 text-muted">
                No completed participants for this trek yet.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useToast } from "vue-toastification"

export default {
  name: 'StaffCompletedBookings',
  props: {
    trekId: {
      type: [Number, String],
      required: true
    }
  },
  setup() {
    const toast = useToast();
    return { toast };
  },
  data() {
    return {
      completedParticipants: []
    }
  },
  mounted() {
    this.fetchCompletedParticipants()
  },
  methods: {
    async fetchCompletedParticipants() {
      try {
        const token = localStorage.getItem('authToken')
        const res = await axios.get(`http://127.0.0.1:5000/api/staff/treks/${this.trekId}/participants`, { 
          headers: { 'Authentication-Token': token }
        })
        this.completedParticipants = res.data.filter(p => p.status === 'Completed')
      } catch (err) { 
        this.toast.error("Failed to load completed history.")
      }
    }
  },
  watch: {
    trekId: 'fetchCompletedParticipants'
  }
}
</script>