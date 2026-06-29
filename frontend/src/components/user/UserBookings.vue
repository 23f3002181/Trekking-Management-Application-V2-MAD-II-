<template>
  <div class="container-fluid py-2">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3 class="fw-bold mb-0">My Bookings</h3>
    </div>

    <div class="card shadow-sm border-0">
      <div class="card-body p-0">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th>Trek Details</th>
              <th>Booking Date</th>
              <th>Status</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="booking in myBookings" :key="booking.booking_id">
              <td>
                <div class="fw-bold">{{ booking.trek_name }}</div>
                <small class="text-muted">📍 {{ booking.location }}</small>
              </td>
              <td>{{ booking.booking_date }}</td>
              <td>
                <span class="badge" 
                      :class="booking.status === 'Booked' ? 'bg-primary' : (booking.status === 'Completed' ? 'bg-success' : 'bg-secondary')">
                  {{ booking.status }}
                </span>
              </td>
              <td class="text-end">
                <!-- Only show Cancel button if the trek is currently Booked -->
                <button 
                  v-if="booking.status === 'Booked'" 
                  class="btn btn-sm btn-outline-danger" 
                  @click="cancelBooking(booking.booking_id)"
                  :disabled="isProcessing === booking.booking_id"
                >
                  {{ isProcessing === booking.booking_id ? 'Cancelling...' : 'Cancel Trek' }}
                </button>
                <button v-else class="btn btn-sm btn-light border" disabled>
                  No Actions
                </button>
              </td>
            </tr>
            <tr v-if="myBookings.length === 0">
              <td colspan="4" class="text-center py-5 text-muted">
                You haven't booked any treks yet.
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
import Swal from 'sweetalert2' // 1. Import SweetAlert

export default {
  setup() {
    const toast = useToast();
    return { toast };
  },
  data() {
    return {
      myBookings: [],
      isProcessing: null
    }
  },
  mounted() {
    this.fetchMyBookings()
  },
  methods: {
    async fetchMyBookings() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/user/bookings')
        this.myBookings = response.data.sort((a, b) => {
          if (a.status === 'Booked' && b.status !== 'Booked') return -1;
          if (a.status !== 'Booked' && b.status === 'Booked') return 1;
          return 0;
        });
      } catch (err) {
        this.toast.error("Failed to load your bookings.");
      }
    },
    
    // 2. The Updated Cancel Method
    async cancelBooking(bookingId) {
      // Fire the SweetAlert confirmation dialog
      const result = await Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to undo this cancellation!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545', // Bootstrap danger red
        cancelButtonColor: '#6c757d',  // Bootstrap secondary grey
        confirmButtonText: 'Yes, cancel it!',
        cancelButtonText: 'No, keep it'
      });

      // If the user clicks "Yes, cancel it!"
      if (result.isConfirmed) {
        this.isProcessing = bookingId;
        
        try {
          const response = await axios.put(`http://127.0.0.1:5000/api/user/bookings/${bookingId}/cancel`);
          
          // SUCCESS TOAST
          this.toast.success(response.data.message || "Booking cancelled.");
          
          await this.fetchMyBookings();
        } catch (err) {
          // ERROR TOAST
          this.toast.error(err.response?.data?.message || 'Error cancelling booking.');
        } finally {
          this.isProcessing = null;
        }
      }
      // If they click cancel, it just silently closes the dialog and does nothing!
    }
  }
}
</script>