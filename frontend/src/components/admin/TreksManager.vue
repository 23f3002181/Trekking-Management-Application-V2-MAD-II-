<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Treks</h2>
      <button class="btn btn-primary" @click="showForm = !showForm">
        {{ showForm ? 'Back to Treks List' : '+ Add New Trek' }}
      </button>
    </div>

    <div v-if="showForm" class="card shadow-sm border-0 mb-4">
      <div class="card-body">
        <form @submit.prevent="createTrek">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label>Trek Name</label>
              <input type="text" class="form-control" v-model="trekForm.name" required>
            </div>
            <div class="col-md-6 mb-3">
              <label>Location</label>
              <input type="text" class="form-control" v-model="trekForm.location" required>
            </div>
            <div class="col-md-4 mb-3">
              <label>Difficulty</label>
              <select class="form-select" v-model="trekForm.difficulty" required>
                <option value="Easy">Easy</option>
                <option value="Moderate">Moderate</option>
                <option value="Hard">Hard</option>
              </select>
            </div>
            <div class="col-md-4 mb-3">
              <label>Duration (Days)</label>
              <input type="number" class="form-control" v-model="trekForm.duration" min="1" required>
            </div>
            <div class="col-md-4 mb-3">
              <label>Available Slots</label>
              <input type="number" class="form-control" v-model="trekForm.slots" min="1" required>
            </div>
          </div>
          <button type="submit" class="btn btn-primary mt-3">Create Trek</button>
          <div v-if="trekMessage" class="alert alert-success mt-3 py-2">{{ trekMessage }}</div>
        </form>
      </div>
    </div>

    <div v-else>
      <div class="mb-3 position-relative" style="max-width: 400px;">
        <i class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
        <input 
          type="text" 
          class="form-control ps-5" 
          placeholder="Search treks by name or location..." 
          v-model="searchQuery"
        >
      </div>

      <div class="card shadow-sm border-0">
        <div class="card-body p-0">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th>ID</th>
                <th>Trek Name</th>
                <th>Location</th>
                <th>Difficulty</th>
                <th>Slots</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="trek in filteredTreks" :key="trek.id">
                <td>{{ trek.id }}</td>
                <td>{{ trek.name }}</td>
                <td>{{ trek.location }}</td>
                <td>{{ trek.difficulty }}</td>
                <td>{{ trek.slots }}</td>
                <td>
                  <span class="badge" :class="trek.status === 'Open' ? 'bg-success' : 'bg-secondary'">
                    {{ trek.status }}
                  </span>
                </td>
              </tr>
              <tr v-if="filteredTreks.length === 0">
                <td colspan="6" class="text-center py-4 text-muted">
                  {{ trekList.length === 0 ? 'No treks created yet.' : 'No treks match your search.' }}
                </td>
              </tr>
            </tbody>
          </table>
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
      showForm: false,
      searchQuery: '',
      trekList: [],
      staffList: [],
      trekForm: { name: '', location: '', difficulty: 'Moderate', duration: 1, slots: 10, staff_id: '' },
      trekMessage: ''
    }
  },
  computed: {
    filteredTreks() {
      // If the search box is empty, return the full list
      if (!this.searchQuery) return this.trekList;
      
      const query = this.searchQuery.toLowerCase();
      
      // Filter by Trek Name OR Location
      return this.trekList.filter(trek => {
        return (
          (trek.name && trek.name.toLowerCase().includes(query)) ||
          (trek.location && trek.location.toLowerCase().includes(query))
        );
      });
    }
  },
  mounted() {
    this.fetchTreksAndStaff()
  },
  methods: {
    async fetchTreksAndStaff() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/admin/treks')
        this.trekList = response.data.treks
        this.staffList = response.data.staff
      } catch (err) {
        console.error("Error fetching treks", err)
      }
    },
    async createTrek() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/admin/treks', this.trekForm)
        this.trekMessage = response.data.message
        this.trekForm = { name: '', location: '', difficulty: 'Moderate', duration: 1, slots: 10, staff_id: '' }
        this.fetchTreksAndStaff()
        setTimeout(() => {
          this.trekMessage = ''
          this.showForm = false // auto hide form after success
        }, 2000)
      } catch (err) {
        this.trekMessage = 'Error creating trek.'
      }
    }
  }
}
</script>