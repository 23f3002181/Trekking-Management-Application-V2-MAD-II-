<template>
  <div class="container mt-4">
    <h2>Admin Dashboard</h2>
    <p>Welcome, Administrator. Milestone 3 functionality will go here.</p>
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