<template>
  <nt-main-pane title="NootTech: More than meets the m-eye-nd" >
    <NtAuthenticatedPane v-if="$store.state.user.authenticated && tokenVerified()"/>
    <NtUnAuthenticatedPane v-else />
  </nt-main-pane>
</template>

<script>
import NtMainPane from './Navigation/MainPane.vue';
import NtAuthenticatedPane from './Navigation/AuthenticatedPane';
import NtUnAuthenticatedPane from './Navigation/UnAuthenticatedPane';

export default {
    name: "Base",
    components: {NtAuthenticatedPane, NtUnAuthenticatedPane, NtMainPane},
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
