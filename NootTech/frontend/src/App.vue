<template>
  <div>
    <nt-navbar></nt-navbar>
        <nt-main-pane title="NootTech: More than meets the m-eye-nd">
          <b-jumbotron header="Discover NooTech!"
                  class="bg-dark"
                  lead="This is a simple hero unit">
            <b-button variant="primary" href="#">More Info</b-button>
          </b-jumbotron>
        </nt-main-pane>
  </div>
</template>

<script>
import NtNavbar from './components/Navigation/Navbar.vue'
import NtMainPane from './components/Navigation/MainPane.vue'

export default {
  name: 'app',
  data: function () {},
  components: {
    NtNavbar, NtMainPane
  },

}
</script>
