<template>
  <div class="container-fluid py-2">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3 class="fw-bold mb-0">Trekking History</h3>
      <button class="btn btn-outline-primary fw-bold" @click="exportCSV" :disabled="isExporting">
        <span class="me-2">📥</span> {{ isExporting ? 'Generating...' : 'Export History (CSV)' }}
      </button>
    </div>

    <div class="card shadow-sm border-0 mb-4">
      <div class="card-body p-0">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th class="ps-4">Trek Name</th>
              <th>Booking Date</th>
              <th>Trek Dates</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="booking in pastBookings" :key="booking.booking_id">
              <td class="fw-bold ps-4">{{ booking.trek_name }}</td>
              <td>{{ booking.booking_date }}</td>
              <td>{{ booking.start_date }} - {{ booking.end_date }}</td>
              <td>
                <span class="badge text-dark bg-light border">{{ booking.status }}</span>
              </td>
            </tr>
            <tr v-if="pastBookings.length === 0">
              <td colspan="3" class="text-center py-4 text-muted">No past history found.</td>
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
  setup() {
    const toast = useToast();
    return { toast }
  },
  data() {
    return {
      myBookings: [],
      isExporting: false
    }
  },
  computed: {
    pastBookings() {
      return this.myBookings.filter(b => b.status === 'Completed' || b.status === 'Cancelled');
    }
  },
  mounted() {
    this.fetchMyBookings()
  },
  methods: {
    async fetchMyBookings() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/user/bookings')
        this.myBookings = res.data
      } catch (err) {
        this.toast.error("Failed to load history.");
      }
    },
    async exportCSV() {
      this.isExporting = true;
      this.toast.info("Exporting your history... Please wait.");

      try {
        const response = await axios.post('http://127.0.0.1:5000/api/user/export');
        const taskId = response.data.task_id;

        const pollInterval = setInterval(async () => {
          try {
            const statusRes = await axios.get(`http://127.0.0.1:5000/api/user/export/status/${taskId}?t=${Date.now()}`, {
              responseType: 'blob',
              headers: {
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
              }
            });

            if (statusRes.status === 200) {
              clearInterval(pollInterval);

              const url = window.URL.createObjectURL(new Blob([statusRes.data]));
              const link = document.createElement('a');
              link.href = url;
              link.setAttribute('download', 'My_Trekking_History.csv');
              document.body.appendChild(link);
              link.click();

              this.isExporting = false;
              this.toast.success("Export completed successfully!");
            }
          } catch (pollErr) {
            
          }
        }, 2000);

      } catch (err) {
        this.isExporting = false;
        this.toast.error("Failed to start export.");
      }
    }
  }
}
</script>