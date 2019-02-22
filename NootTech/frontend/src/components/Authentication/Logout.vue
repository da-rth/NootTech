<template>
</template>

<script>

export default {
  name: 'Logout',
  mounted () {
    let redirect = decodeURIComponent(this.$route.query.redirect || '/')
    console.log("ARE YOU LOGGING OUT?!");
    this.$store.commit('LOGOUT', {
      redirect: redirect
    })
  }
}
</script>

<style scoped>
</style>
