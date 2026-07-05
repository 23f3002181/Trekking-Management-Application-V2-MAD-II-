<template>
  <div class="landing-page bg-light min-vh-100">

    <!-- 1. NAVBAR -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top shadow-sm">
      <div class="container">
        <a class="navbar-brand fw-bold d-flex align-items-center" href="#">
          <span class="fs-3 me-2"><i class="bi bi-backpack4-fill"></i></span> TrekApp
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0 align-items-center">
            <li class="nav-item">
              <a class="nav-link active" href="#">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#popular-treks">Top Treks</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#analytics">Live Stats</a>
            </li>

            <li class="nav-item ms-lg-3 mt-3 mt-lg-0">
              <router-link v-if="!isLoggedIn" to="/login" class="btn btn-outline-light px-4 rounded-pill">
                Login / Register
              </router-link>

              <div v-else class="d-flex gap-2">
                <router-link to="/user-dashboard" class="btn btn-light rounded-pill px-4">
                  My Dashboard
                </router-link>
                <button @click="handleLogout" class="btn btn-outline-danger rounded-pill px-4">
                  Logout
                </button>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- 2. HERO SECTION -->
    <header class="hero-section position-relative d-flex align-items-center text-center">
      <div class="overlay"></div>
      <div class="container position-relative z-1 text-white">
        <h1 class="display-3 fw-bolder mb-3 text-shadow">Find Your Next Adventure</h1>
        <p class="lead mx-auto mb-5 text-light text-shadow" style="max-width: 700px;">
          Join thousands of trekkers exploring the world's most breathtaking trails. Experience nature like never before
          with expert-led routes and seamless booking.
        </p>
        <router-link v-if="!isLoggedIn" to="/login"
          class="btn btn-success btn-lg px-5 py-3 rounded-pill fw-bold shadow-lg hero-btn">
          Start Exploring
        </router-link>
        <a v-else href="#popular-treks"
          class="btn btn-success btn-lg px-5 py-3 rounded-pill fw-bold shadow-lg hero-btn">
          View Top Treks
        </a>
      </div>
    </header>

    <!-- 3. FEATURES SECTION -->
    <section class="py-5 bg-light">
      <div class="container py-4">
        <div class="row text-center g-4">
          <div class="col-md-4">
            <div class="feature-card p-4 rounded-4">
              <div class="icon-wrapper bg-success bg-opacity-10 text-success mb-3 mx-auto">
                <i class="bi bi-geo-alt fs-2"></i>
              </div>
              <h4 class="fw-bold">Stunning Locations</h4>
              <p class="text-muted">Explore carefully curated routes ranging from serene valleys to challenging mountain
                peaks.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card p-4 rounded-4">
              <div class="icon-wrapper bg-primary bg-opacity-10 text-primary mb-3 mx-auto">
                <i class="bi bi-shield-check fs-2"></i>
              </div>
              <h4 class="fw-bold">Expert Led</h4>
              <p class="text-muted">Every trek is guided by our certified and experienced trekking staff for your
                safety.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card p-4 rounded-4">
              <div class="icon-wrapper bg-warning bg-opacity-10 text-warning mb-3 mx-auto">
                <i class="bi bi-calendar-check fs-2"></i>
              </div>
              <h4 class="fw-bold">Instant Booking</h4>
              <p class="text-muted">Check live availability, secure your slots, and manage your trips entirely online.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 4. POPULAR TREKS SLIDER -->
    <section id="popular-treks" class="py-3 bg-light" v-if="popularTreksList.length > 0">
      <div class="container">
        <div class="d-flex justify-content-between align-items-end mb-4">
          <div>
            <h2 class="display-6 fw-bold text-dark mb-0">Trending Trails</h2>
            <p class="text-muted mt-2 mb-0">Our most booked adventures right now.</p>
          </div>
          <div class="d-none d-md-block text-muted small explore-btn" @click="scrollToEnd" style="cursor: pointer;">
            Swipe to explore <i class="bi bi-arrow-right ms-1"></i>
          </div>
        </div>

        <div class="scrolling-wrapper row flex-row flex-nowrap pb-4 pt-2" ref="trekSlider">
          <div class="col-10 col-sm-6 col-md-4 col-lg-3" v-for="(trek, index) in popularTreksList" :key="index">
            <div class="card shadow-sm h-100 border-0 rounded-4 overflow-hidden trek-card">
              <img :src="trek.image" class="card-img-top" :alt="trek.name" style="height: 220px; object-fit: cover;">
              <div class="card-body d-flex flex-column">
                <h5 class="card-title fw-bold text-truncate">{{ trek.name }}</h5>
                <p class="card-text text-muted small mb-4">
                  <i class="bi bi-fire text-danger me-1"></i> {{ trek.bookings }} Adventurers booked
                </p>
                <router-link v-if="!isLoggedIn" to="/login"
                  class="btn btn-outline-success w-100 rounded-pill mt-auto fw-bold">
                  Explore Trek
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 5. ANALYTICS SECTION -->
    <section id="analytics" class="py-5 bg-light">
      <div class="container text-center mb-5">
        <h2 class="display-4 fw-bold text-dark">Platform Transparency</h2>
        <p class="display-6 text-muted">We believe in open data. Check out our real-time community statistics.</p>
      </div>

      <div class="container pb-5">
        <div class="row g-4">
          <!-- Popular Treks Chart -->
          <div class="col-md-6">
            <div class="card shadow-sm h-100 border-0 rounded-4 overflow-hidden stat-card">
              <div class="card-header bg-white border-bottom-0 pt-4 pb-0 text-center">
                <h5 class="mb-0 fw-bold text-secondary"><i class="bi bi-bar-chart-line text-danger me-2"></i> Booking
                  Volume</h5>
              </div>
              <div class="card-body chart-container p-4">
                <Bar v-if="loaded" :data="barChartData" :options="chartOptions" />
                <div v-else class="d-flex justify-content-center align-items-center h-100 mt-4">
                  <div class="spinner-border text-success" role="status"><span class="visually-hidden">Loading...</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Availability Chart -->
          <div class="col-md-6">
            <div class="card shadow-sm h-100 border-0 rounded-4 overflow-hidden stat-card">
              <div class="card-header bg-white border-bottom-0 pt-4 pb-0 text-center">
                <h5 class="mb-0 fw-bold text-secondary"><i class="bi bi-pie-chart text-primary me-2"></i> Trek
                  Availability</h5>
              </div>
              <div class="card-body chart-container p-4">
                <Pie v-if="loaded" :data="pieChartData" :options="chartOptions" />
                <div v-else class="d-flex justify-content-center align-items-center h-100 mt-4">
                  <div class="spinner-border text-success" role="status"><span class="visually-hidden">Loading...</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Line Chart -->
          <div class="col-12">
            <div class="card shadow-sm border-0 rounded-4 overflow-hidden stat-card">
              <div class="card-header bg-white border-bottom-0 pt-4 pb-0 text-center">
                <h5 class="mb-0 fw-bold text-secondary"><i class="bi bi-graph-up-arrow text-success me-2"></i> Monthly
                  Participation Trends</h5>
              </div>
              <div class="card-body chart-container p-4" style="height: 400px;">
                <Line v-if="loaded" :data="lineChartData" :options="lineChartOptions" />
                <div v-else class="d-flex justify-content-center align-items-center h-100 mt-4">
                  <div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 6. FOOTER -->
    <footer class="bg-dark text-white pt-5 pb-3">
      <div class="container">
        <div class="row gy-4">
          <div class="col-md-4">
            <h5 class="fw-bold mb-3 d-flex align-items-center"><span class="fs-4 me-2">🏔️</span> TrekApp</h5>
            <p class="text-white-50 small">
              Making adventure accessible, safe, and unforgettable. Join the community and step into the wild.
            </p>
          </div>
          <div class="col-md-4">
            <h5 class="fw-bold mb-3">Quick Links</h5>
            <ul class="list-unstyled text-white-50 small lh-lg">
              <li><a href="#" class="text-decoration-none text-white-50 hover-white">About Us</a></li>
              <li><a href="#" class="text-decoration-none text-white-50 hover-white">All Treks</a></li>
              <li><a href="#" class="text-decoration-none text-white-50 hover-white">Safety Guidelines</a></li>
              <li><a href="#" class="text-decoration-none text-white-50 hover-white">Contact Support</a></li>
            </ul>
          </div>
          <div class="col-md-4">
            <h5 class="fw-bold mb-3">Connect</h5>
            <div class="d-flex gap-3">
              <a href="#" class="text-white-50 hover-white fs-4"><i class="bi bi-facebook"></i></a>
              <a href="#" class="text-white-50 hover-white fs-4"><i class="bi bi-instagram"></i></a>
              <a href="#" class="text-white-50 hover-white fs-4"><i class="bi bi-twitter-x"></i></a>
            </div>
          </div>
        </div>
        <hr class="border-secondary mt-4 mb-3">
        <div class="text-center text-white-50 small">
          &copy; 2026 TrekApp. All rights reserved.
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';
import { Bar, Pie, Line } from 'vue-chartjs'
import {
  Chart as ChartJS, Title, Tooltip, Legend, BarElement,
  CategoryScale, LinearScale, ArcElement, LineElement, PointElement
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement, LineElement, PointElement)

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
      popularTreksList: [], // NEW: Holds the mapped data for the slider
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
        tension: 0.4,
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

      // UPDATE: Map the analytics data to build the slider cards dynamically
      if (data.popular_treks && data.popular_treks.labels) {
        this.popularTreksList = data.popular_treks.labels.map((trekName, index) => ({
          name: trekName,
          bookings: data.popular_treks.data[index],
          // NEW: Grab the image directly from the API response
          image: data.popular_treks.images[index]
        }));
      }

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
          label: 'Trekkers Participated', borderColor: '#0d6efd', backgroundColor: 'rgba(13, 110, 253, 0.1)', borderWidth: 3, fill: true, data: data.booking_trends.data
        }]
      };

      this.loaded = true;
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  },
  methods: {
    async handleLogout() {
      const result = await Swal.fire({
        title: 'Ready to leave?',
        text: "You are about to log out of your account.",
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Logout'
      })

      if (result.isConfirmed) {
        localStorage.removeItem('authToken');
        this.isLoggedIn = false;
        Toast.fire({ icon: 'success', title: 'Successfully logged out.' });
      }
    },
    scrollToEnd() {
      const slider = this.$refs.trekSlider;
      if (slider) {
        // Scroll to the maximum width of the container smoothly
        slider.scrollTo({
          left: slider.scrollWidth,
          behavior: 'smooth'
        });
      }
    }
  }
}
</script>

<style scoped>
.landing-page {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  scroll-behavior: smooth;
}

/* Hero Section */
.hero-section {
  min-height: 80vh;
  background-image: url('https://images.unsplash.com/photo-1522199755839-a2bacb67c546?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.4) 0%, rgba(0, 0, 0, 0.7) 100%);
  z-index: 0;
}

.text-shadow {
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
}

.hero-btn {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hero-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(25, 135, 84, 0.4) !important;
}

/* Feature Cards */
.feature-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid transparent;
  box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.08);
  border-color: #f8f9fa;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.icon-wrapper {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Scrolling Wrapper (Netflix Style Slider) */
.scrolling-wrapper {
  overflow-x: auto;
  overflow-y: hidden;
  white-space: nowrap;
  -webkit-overflow-scrolling: touch;
  scroll-snap-type: x mandatory;
  padding-bottom: 20px;
  /* Space for shadow */
}

/* Hide scrollbar for clean UI */
.scrolling-wrapper::-webkit-scrollbar {
  display: none;
}

.scrolling-wrapper {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scrolling-wrapper>div {
  scroll-snap-align: start;
}

.trek-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  white-space: normal;
  /* Fix text wrapping inside cards */
}

.trek-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1) !important;
}

/* Chart Cards */
.stat-card {
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05) !important;
}

.chart-container {
  position: relative;
  min-height: 300px;
}

/* Footer Links */
.hover-white {
  transition: color 0.2s ease;
}

.hover-white:hover {
  color: #fff !important;
}

.explore-btn {
  transition: color 0.2s ease;
}

.explore-btn:hover {
  color: #198754 !important;
}
</style>