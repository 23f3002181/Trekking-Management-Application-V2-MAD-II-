<template>
  <div>    
    <div class="row mb-5">
      <div class="col-md-4">
        <div class="card shadow-sm border-0 text-center py-3">
          <h6 class="text-muted">Assigned Treks</h6>
          <h2 class="mb-0">{{ stats.assigned_treks }} <i class="bi bi-calendar ms-2 text-secondary"></i></h2>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card shadow-sm border-0 text-center py-3">
          <h6 class="text-muted">Total Participants</h6>
          <h2 class="mb-0">{{ stats.total_participants }} <i class="bi bi-people ms-2 text-secondary"></i></h2>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card shadow-sm border-0 text-center py-3">
          <h6 class="text-muted">Ongoing Treks</h6>
          <h2 class="mb-0">{{ stats.ongoing_treks }} <i class="bi bi-signpost-split ms-2 text-secondary"></i></h2>
        </div>
      </div>
    </div>

    <h5 class="mb-3">My Assigned Treks</h5>
    <div class="card shadow-sm border-0">
      <div class="card-body p-0">
        <table class="table table-hover mb-0 align-middle">
          <thead class="table-light">
            <tr>
              <th>Trek Name</th>
              <th>Dates</th>
              <th>Participants</th>
              <th>Slots</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="trek in treks" :key="trek.id">
              <td><strong>{{ trek.name }}</strong></td>
              <td>{{ trek.start_date }} - {{ trek.end_date }}</td>
              <td>{{ trek.participants }}</td>
              <td>{{ trek.total_slots }}</td>
              <td>
                <span class="badge" :class="trek.status === 'Open' ? 'bg-success' : 'bg-secondary'">
                  {{ trek.status }}
                </span>
              </td>
              <td>
                <router-link :to="`/staff-dashboard/manage/${trek.id}`" class="btn btn-sm btn-outline-primary px-3">
                  {{ trek.status === 'Open' ? 'Manage' : 'View' }}
                </router-link>
              </td>
            </tr>
            <tr v-if="treks.length === 0">
              <td colspan="6" class="text-center py-4">No treks assigned yet.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      stats: { assigned_treks: 0, total_participants: 0, ongoing_treks: 0 },
      treks: []
    }
  },
  mounted() {
    this.fetchStats()
    this.fetchTreks()
  },
  methods: {
    async fetchStats() {
      try {
        const token = localStorage.getItem('authToken')
        const res = await axios.get('http://127.0.0.1:5000/api/staff/stats', { headers: { 'Authentication-Token': token }})
        this.stats = res.data
      } catch (err) { console.error(err) }
    },
    async fetchTreks() {
      try {
        const token = localStorage.getItem('authToken')
        const res = await axios.get('http://127.0.0.1:5000/api/staff/treks', { headers: { 'Authentication-Token': token }})
        this.treks = res.data
      } catch (err) { console.error(err) }
    }
  }
}
</script>