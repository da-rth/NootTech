<template>
  <footer class="page-footer text-light">
    <div class="footer-copyright text-center py-3">
      <router-link to="/privacy"><font-awesome-icon icon="shield-alt"/>&nbsp; Privacy Policy</router-link>
      &nbsp;&nbsp;|&nbsp;&nbsp;
      <router-link to="/"><a><font-awesome-icon icon="copyright"/>&nbsp; 2019 Noot.Tech</a></router-link>
      &nbsp;&nbsp;|&nbsp;&nbsp;
      <router-link to="/terms"><font-awesome-icon icon="info-circle"/>&nbsp; Terms of Service</router-link>
    </div>
  </footer>
</template>

<script>
    export default {
        name: "NtFooter"
    }
</script>
