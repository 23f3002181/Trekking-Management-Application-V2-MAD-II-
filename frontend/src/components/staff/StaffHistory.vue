<template>
  <div>
    <h2 class="mb-4">Completed Bookings History</h2>
    <p class="text-muted mb-4">A complete record of participants from your finalized treks.</p>
    
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-success" role="status"></div>
    </div>

    <div v-else class="card shadow-sm border-0 border-success border-start border-4">
      <div class="card-body p-0">
        <table class="table table-hover mb-0 align-middle">
          <thead class="table-light">
            <tr>
              <th class="ps-4">Trek Name</th>
              <th>Participant Name</th>
              <th>Email</th>
              <th>Booking Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in historyList" :key="p.booking_id">
              <td class="ps-4"><strong>{{ p.trek_name }}</strong></td>
              <td>{{ p.user_name }}</td>
              <td>{{ p.user_email }}</td>
              <td>{{ p.booking_date }}</td>
              <td><span class="badge bg-success">Completed</span></td>
            </tr>
            
            <tr v-if="historyList.length === 0">
              <td colspan="5" class="text-center py-5 text-muted">
                <i class="bi bi-clock-history fs-1 d-block mb-3"></i>
                No completed bookings found yet.
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
  name: 'StaffHistory',
  setup() {
    const toast = useToast();
    return { toast };
  },
  data() {
    return {
      historyList: [],
      isLoading: true
    }
  },
  mounted() {
    this.fetchAllCompletedBookings()
  },
  methods: {
    async fetchAllCompletedBookings() {
      try {
        const token = localStorage.getItem('authToken');
        
        // Call the new dedicated history route!
        const res = await axios.get('http://127.0.0.1:5000/api/staff/history', {
          headers: { 'Authentication-Token': token }
        });
        
        this.historyList = res.data;
        
      } catch (err) { 
        this.toast.error("Failed to load completed history.");
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>