<template>
  <div>
    <nt-navbar></nt-navbar>
    <nt-main-pane title="NootTech: More than meets the m-eye-nd">
      <p>Hi there</p>
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
