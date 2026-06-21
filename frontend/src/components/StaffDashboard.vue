<template>
  <div class="container mt-4">
    <h2>Staff Dashboard</h2>
    <p>Welcome, Trek Staff. Milestone 4 functionality will go here.</p>
    <button class="btn btn-danger" @click="logout">Logout</button>
  </div>
</template>

<script>
export default {
  methods: {
    logout() {
      localStorage.removeItem('authToken')
      this.$router.push('/')
    }
  }
}
</script>