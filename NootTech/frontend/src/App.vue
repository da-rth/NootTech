<template>
  <div>
    <nt-navbar></nt-navbar>
    <nt-main-pane>
     <H3>
      This information is being displayed by VueJS but taken from
      <a v-bind:href="this.$api_url+'/list-users/'">this API url</a>
    </H3>

   </nt-main-pane>
  </div>
</template>

<script>
import NtNavbar from './components/Navigation/Navbar.vue'
import NtMainPane from './components/Navigation/MainPane.vue'

export default {
  name: 'app',
  data() {},
  components: {
    NtNavbar, NtMainPane
  },

}
</script>
