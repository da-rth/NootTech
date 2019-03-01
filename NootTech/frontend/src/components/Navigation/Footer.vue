<template>
  <footer class="page-footer text-light">
    <div class="footer-copyright text-center py-3">
      <router-link to="/privacy"><font-awesome-icon icon="shield-alt"/> Privacy Policy</router-link>
      &nbsp;&nbsp;|&nbsp;&nbsp;
      <router-link to="/"><font-awesome-icon icon="copyright"/> 2019 Copyright: Noot.Tech</router-link>
      &nbsp;&nbsp;|&nbsp;&nbsp;
      <router-link to="/terms"><font-awesome-icon icon="info-circle"/> Terms of Service</router-link>
    </div>
  </footer>
</template>

<script>
    export default {
        name: "NtFooter"
    }
</script>
