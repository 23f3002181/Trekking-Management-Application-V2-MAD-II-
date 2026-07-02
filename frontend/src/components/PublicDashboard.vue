<template>
  <div class="landing-page bg-light min-vh-100">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
      <div class="container">
        <a class="navbar-brand fw-bold" href="#">🏔️ TrekApp</a>
        <div class="d-flex ms-auto gap-2">
          
          <router-link v-if="!isLoggedIn" to="/login" class="btn btn-outline-light px-4">
            Login / Register
          </router-link>

          <template v-else>
            <button @click="handleLogout" class="btn btn-outline-danger px-4">
              Logout
            </button>
          </template>

        </div>
      </div>
    </nav>

    <div class="container text-center mt-5 mb-5 pt-4">
      <h1 class="display-4 fw-bold text-dark mb-3">Adventure Awaits.</h1>
      <p class="lead text-muted mx-auto" style="max-width: 600px;">
        Join thousands of trekkers exploring the world's most breathtaking trails. 
        Check out our live platform statistics below and sign in to book your next journey!
      </p>
    </div>
    
    <div class="container pb-5">
      <div class="row">
        <div class="col-md-6 mb-4">
          <div class="card shadow-sm h-100 border-0 rounded-3">
            <div class="card-header bg-white border-bottom-0 pt-4 pb-0">
              <h5 class="mb-0 fw-bold text-secondary">🔥 Most Popular Treks</h5>
            </div>
            <div class="card-body chart-container">
              <Bar v-if="loaded" :data="barChartData" :options="chartOptions" />
              <div v-else class="text-center mt-5 spinner-border text-success" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6 mb-4">
          <div class="card shadow-sm h-100 border-0 rounded-3">
            <div class="card-header bg-white border-bottom-0 pt-4 pb-0">
              <h5 class="mb-0 fw-bold text-secondary">📊 Trek Availability</h5>
            </div>
            <div class="card-body chart-container">
              <Pie v-if="loaded" :data="pieChartData" :options="chartOptions" />
              <div v-else class="text-center mt-5 spinner-border text-success" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row mt-2">
        <div class="col-12 mb-4">
          <div class="card shadow-sm border-0 rounded-3">
            <div class="card-header bg-white border-bottom-0 pt-4 pb-0">
              <h5 class="mb-0 fw-bold text-secondary">📈 Monthly Participation & Booking Trends</h5>
            </div>
            <div class="card-body chart-container" style="height: 400px;">
              <Line v-if="loaded" :data="lineChartData" :options="lineChartOptions" />
              <div v-else class="text-center mt-5 spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2'; // NEW: Import SweetAlert
import { Bar, Pie, Line } from 'vue-chartjs'
import { 
  Chart as ChartJS, Title, Tooltip, Legend, BarElement, 
  CategoryScale, LinearScale, ArcElement, LineElement, PointElement
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement, LineElement, PointElement)

// Setup the reusable Toast
const Toast = Swal.mixin({
  toast: true, position: 'top-end', showConfirmButton: false, timer: 3000, timerProgressBar: true
})

export default {
  name: 'PublicDashboard',
  components: { Bar, Pie, Line },
  data() {
    return {
      isLoggedIn: false, 
      loaded: false,
      barChartData: null,
      pieChartData: null,
      lineChartData: null,
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'bottom' } }
      },
      lineChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        tension: 0.3, 
        plugins: { legend: { position: 'top' } },
        scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
      }
    }
  },
  async mounted() {
    if (localStorage.getItem('authToken')) {
      this.isLoggedIn = true;
    }

    try {
      const response = await axios.get('http://127.0.0.1:5000/api/public/analytics');
      const data = response.data;

      this.barChartData = {
        labels: data.popular_treks.labels,
        datasets: [{
          label: 'Total Bookings', backgroundColor: '#198754', borderRadius: 4, data: data.popular_treks.data
        }]
      };

      this.pieChartData = {
        labels: data.trek_status.labels,
        datasets: [{
          backgroundColor: ['#198754', '#ffc107', '#dc3545', '#0dcaf0', '#6c757d'], borderWidth: 0, data: data.trek_status.data
        }]
      };

      this.lineChartData = {
        labels: data.booking_trends.labels,
        datasets: [{
          label: 'Trekkers Participated', borderColor: '#0d6efd', backgroundColor: 'rgba(13, 110, 253, 0.2)', borderWidth: 3, fill: true, data: data.booking_trends.data
        }]
      };

      this.loaded = true;
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  },
  methods: {
    async handleLogout() {
      // 1. Ask for confirmation
      const result = await Swal.fire({
        title: 'Ready to leave?',
        text: "You are about to log out of your account.",
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Logout'
      })

      // 2. If confirmed, log them out and show Toast
      if (result.isConfirmed) {
        localStorage.removeItem('authToken');
        this.isLoggedIn = false;
        Toast.fire({ icon: 'success', title: 'Successfully logged out.' });
      }
    }
  }
}
</script>

<style scoped>
.chart-container {
  position: relative;
  padding: 1rem;
}
.landing-page {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
</style>