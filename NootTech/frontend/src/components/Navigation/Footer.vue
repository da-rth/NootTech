<template>
<!-- Footer -->
<footer class="page-footer text-light">
  <!-- Copyright -->
  <div class="footer-copyright text-center py-3"><font-awesome-icon :icon="['far', 'copyright']"/>
    <router-link to="/privacy"><font-awesome-icon :icon="['fas', 'shield-alt']"/> Privacy Policy</router-link>
    &nbsp;&nbsp;|&nbsp;&nbsp;
    <router-link to="/"><font-awesome-icon :icon="['fas', 'copyright']"/> 2019 Copyright: Noot.Tech</router-link>
    &nbsp;&nbsp;|&nbsp;&nbsp;
    <router-link to="/terms"><font-awesome-icon :icon="['fas', 'info-circle']"/> Terms of Service</router-link>
  </div>
  <!-- Copyright -->

</footer>
<!-- Footer -->
</template>

<script>
    export default {
        name: "NtFooter"
    }
</script>

<style scoped>
  .footer-copyright {
    font-size: 0.8em;
    background-color: #242424;
    padding-top: 10px;
    padding-bottom: 0px;
    position:fixed;
    bottom:0;
    width:100%;
    opacity: 0.9;
}
</style>
