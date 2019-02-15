<template>
  <div id="NTapp">
    <nt-navbar></nt-navbar>
    <router-view/>
    <nt-footer></nt-footer>
  </div>
</template>

<script>
import NtNavbar from './components/Navigation/Navbar.vue'
import NtMainPane from './components/Navigation/MainPane.vue'
import NtFooter from './components/Navigation/Footer.vue'

export default {
  name: 'app',
  data: function () {},
  components: {
    NtNavbar, NtMainPane, NtFooter
  },

}
</script>
