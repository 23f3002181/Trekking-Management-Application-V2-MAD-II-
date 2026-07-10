<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Treks</h2>
      <button class="btn btn-primary" @click="toggleForm">
        {{ showForm ? 'Back to Treks List' : '+ Add New Trek' }}
      </button>
    </div>

    <div v-if="showForm" class="card shadow-sm border-0 mb-4">
      <div class="card-header bg-white pt-3 pb-0 border-0">
        <h5 class="mb-0 text-primary">{{ isEditing ? 'Edit Trek Route' : 'Create New Trek' }}</h5>
      </div>
      <div class="card-body">
        <form @submit.prevent="isEditing ? updateTrek() : createTrek()">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label>Trek Name</label>
              <input type="text" class="form-control" v-model="trekForm.name" required>
            </div>
            <div class="col-md-6 mb-3">
              <label>Location</label>
              <input type="text" class="form-control" v-model="trekForm.location" required>
            </div>
            <div class="col-md-3 mb-3">
              <label>Difficulty</label>
              <select class="form-select" v-model="trekForm.difficulty" required>
                <option value="Easy">Easy</option>
                <option value="Moderate">Moderate</option>
                <option value="Hard">Hard</option>
              </select>
            </div>
            <div class="col-md-3 mb-3">
              <label>Duration (Days)</label>
              <input type="number" class="form-control" v-model="trekForm.duration" min="1" required>
            </div>
            <div class="col-md-3 mb-3">
              <label>Total Slots</label>
              <input type="number" class="form-control" v-model="trekForm.total_slots" min="1" required>
            </div>
            <div class="col-md-3 mb-3">
              <label>Assign Staff (Optional)</label>
              <select class="form-select" v-model="trekForm.staff_id">
                <option value="">-- Unassigned --</option>
                <option v-for="staff in staffList" :key="staff.id" :value="staff.id">
                  {{ staff.name }}
                </option>
              </select>
            </div>
            <div class="col-md-12 mb-3">
              <label>Trek Image</label>
              <input type="file" class="form-control" @change="handleFileUpload" accept="image/*">
            </div>
          </div>
          <button type="submit" class="btn mt-3" :class="isEditing ? 'btn-warning' : 'btn-primary'">
            {{ isEditing ? 'Update Trek' : 'Create Trek' }}
          </button>
        </form>
      </div>
    </div>

    <div v-else>
      <div class="mb-3 position-relative" style="max-width: 400px;">
        <i class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
        <input type="text" class="form-control ps-5" placeholder="Search treks..." v-model="searchQuery">
      </div>

      <div v-if="toastMsg" class="alert alert-info py-2 shadow-sm border-0 position-absolute"
        style="top: 20px; right: 20px; z-index: 1050;">
        <i class="bi bi-check-circle-fill me-2 text-success"></i> {{ toastMsg }}
      </div>

      <div class="card shadow-sm border-0">
        <div class="card-body p-0">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>ID</th>
                <th>Trek Name</th>
                <th>Difficulty</th>
                <th>Duration</th>
                <th>Total Slots</th>
                <th>Available Slots</th>
                <th>Status</th>
                <th>Assigned Staff</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="trek in filteredTreks" :key="trek.id">
                <td>{{ trek.id }}</td>
                <td><strong>{{ trek.name }}</strong><br><small class="text-muted">{{ trek.location }}</small></td>
                <td>{{ trek.difficulty }}</td>
                <td>{{ trek.duration }} Days</td>
                <td>{{ trek.total_slots }}</td>
                <td>{{ trek.available_slots }}</td>
                <td>
                  <span class="badge" :class="trek.status === 'Open' ? 'bg-success' : 'bg-secondary'">{{ trek.status
                  }}</span>
                </td>
                <td>
                  <select class="form-select form-select-sm" v-model="trek.staff_id"
                    @change="assignStaff(trek.id, trek.staff_id)">
                    <option :value="null">-- Unassigned --</option>
                    <option v-for="staff in staffList" :key="staff.id" :value="staff.id">
                      {{ staff.name }}
                    </option>
                  </select>
                </td>
                <td>
                  <div class="d-flex gap-2">
                    <button class="btn btn-sm btn-outline-primary" @click="editTrek(trek)" title="Edit">
                      <i class="bi bi-pencil"></i> Edit
                    </button>
                    <button class="btn btn-sm btn-outline-danger" @click="deleteTrek(trek)" title="Delete">
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredTreks.length === 0">
                <td colspan="7" class="text-center py-4 text-muted">No treks match your search.</td>
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
import Swal from 'sweetalert2'

const Toast = Swal.mixin({
  toast: true,
  position: 'top-end',
  showConfirmButton: false,
  timer: 3000,
  timerProgressBar: true,
  didOpen: (toast) => {
    toast.addEventListener('mouseenter', Swal.stopTimer)
    toast.addEventListener('mouseleave', Swal.resumeTimer)
  }
})

export default {
  data() {
    return {
      showForm: false,
      isEditing: false, 
      editingTrekId: null, 
      searchQuery: '',
      trekList: [],
      staffList: [],
      selectedFile: null,
      toastMsg: '', 
      trekForm: { name: '', location: '', difficulty: 'Moderate', duration: 1, total_slots: 10, available_slots: 10, staff_id: '' }
    }
  },
  computed: {
    filteredTreks() {
      let activeTreks = this.trekList.filter(t => t.status !== 'Completed');

      if (!this.searchQuery) return activeTreks;

      const q = this.searchQuery.toLowerCase();
      return activeTreks.filter(t => t.name.toLowerCase().includes(q) || t.location.toLowerCase().includes(q));
    }
  },
  mounted() {
    this.fetchTreks()
  },
  methods: {
    toggleForm() {
      this.showForm = !this.showForm;
      if (!this.showForm) {
        this.resetForm();
      }
    },
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    resetForm() {
      this.isEditing = false;
      this.editingTrekId = null;
      this.selectedFile = null;
      this.trekForm = { name: '', location: '', difficulty: 'Moderate', duration: 1, total_slots: 10, available_slots: 10, staff_id: '' };
    },
    async fetchTreks() {
      try {
        const token = localStorage.getItem('authToken')
        const res = await axios.get('http://127.0.0.1:5000/api/admin/treks', {
          headers: { 'Authentication-Token': token }
        })
        this.trekList = res.data.treks
        this.staffList = res.data.staff
      } catch (err) {
        console.error(err)
      }
    },
    async createTrek() {
      try {
        const token = localStorage.getItem('authToken')
        const formData = new FormData();
        formData.append('name', this.trekForm.name);
        formData.append('location', this.trekForm.location);
        formData.append('difficulty', this.trekForm.difficulty);
        formData.append('duration', this.trekForm.duration);
        formData.append('total_slots', this.trekForm.total_slots);
        formData.append('staff_id', this.trekForm.staff_id || '');

        if (this.selectedFile) {
          formData.append('image', this.selectedFile);
        }

        const res = await axios.post('http://127.0.0.1:5000/api/admin/treks', formData, {
          headers: { 'Authentication-Token': token }
        })

        Toast.fire({ icon: 'success', title: res.data.message })
        this.resetForm()
        this.fetchTreks()
        this.showForm = false
      } catch (err) {
        Toast.fire({ icon: 'error', title: 'Failed to create Trek route.' })
      }
    },
    editTrek(trek) {
      this.isEditing = true;
      this.editingTrekId = trek.id;
      this.trekForm = {
        name: trek.name,
        location: trek.location,
        difficulty: trek.difficulty,
        duration: trek.duration,
        available_slots: trek.available_slots,
        total_slots: trek.total_slots,
        staff_id: trek.staff_id || ''
      };
      this.showForm = true;
    },
    async updateTrek() {
      try {
        const token = localStorage.getItem('authToken')
        const formData = new FormData();
        formData.append('name', this.trekForm.name);
        formData.append('location', this.trekForm.location);
        formData.append('difficulty', this.trekForm.difficulty);
        formData.append('duration', this.trekForm.duration);
        formData.append('total_slots', this.trekForm.total_slots);
        formData.append('staff_id', this.trekForm.staff_id || '');

        if (this.selectedFile) {
          formData.append('image', this.selectedFile);
        }
        await axios.put(`http://127.0.0.1:5000/api/admin/treks/${this.editingTrekId}`, formData, {
          headers: { 'Authentication-Token': token }
        })

        Toast.fire({ icon: 'success', title: 'Trek updated successfully!' })
        this.resetForm()
        this.fetchTreks()
        this.showForm = false
      } catch (err) {
        Toast.fire({ icon: 'error', title: 'Failed to update trek.' })
      }
    },
    async deleteTrek(trek) {
      const result = await Swal.fire({
        title: 'Delete this trek?',
        text: `You are about to delete "${trek.name}". This cannot be undone!`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Yes, delete it!'
      })

      if (result.isConfirmed) {
        try {
          const token = localStorage.getItem('authToken')
          await axios.delete(`http://127.0.0.1:5000/api/admin/treks/${trek.id}`, {
            headers: { 'Authentication-Token': token }
          })

          Toast.fire({ icon: 'success', title: 'Trek deleted successfully.' })
          this.fetchTreks()
        } catch (err) {
          Toast.fire({ icon: 'error', title: 'Error: Cannot delete a trek with active bookings.' })
        }
      }
    },
    async assignStaff(trekId, staffId) {
      try {
        const token = localStorage.getItem('authToken')
        await axios.put(`http://127.0.0.1:5000/api/admin/treks/${trekId}/assign`,
          { staff_id: staffId },
          { headers: { 'Authentication-Token': token } }
        )
        Toast.fire({ icon: 'success', title: 'Staff assigned successfully!' })
      } catch (err) {
        Toast.fire({ icon: 'error', title: 'Failed to assign staff.' })
      }
    }
  }
}
</script>