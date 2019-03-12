<template>
  <NtAuthenticatedPane v-if="$store.state.user && tokenVerified()"/>
  <NtUnAuthenticatedPane v-else />
</template>

<script>
import NtAuthenticatedPane from './Navigation/AuthenticatedPane';
import NtUnAuthenticatedPane from './Navigation/UnAuthenticatedPane';

export default {
    name: "Base",
    components: {NtAuthenticatedPane, NtUnAuthenticatedPane},
    methods: {
      tokenVerified() {
        if (this.$store.state.token) {
          return true
        } else {
          return false
        }
      }
    }
}
</script>

<style scoped>

</style>
