<template>
  <div id="NTapp">
    <nt-navbar></nt-navbar>
    <br/>
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
  }

}
</script>

<style>
    body {
    background-color: #242424;
  }

  h1 {
    color: white;
  }
</style>
