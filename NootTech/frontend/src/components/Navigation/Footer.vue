<template>
  <footer class="page-footer text-light">
    <div class="footer-copyright text-center py-3"><font-awesome-icon :icon="['far', 'copyright']"/>
      <router-link to="/privacy"><font-awesome-icon :icon="['fas', 'shield-alt']"/> Privacy Policy</router-link>
      &nbsp;&nbsp;|&nbsp;&nbsp;
      <router-link to="/"><font-awesome-icon :icon="['fas', 'copyright']"/> 2019 Copyright: Noot.Tech</router-link>
      &nbsp;&nbsp;|&nbsp;&nbsp;
      <router-link to="/terms"><font-awesome-icon :icon="['fas', 'info-circle']"/> Terms of Service</router-link>
    </div>
  </footer>
</template>

<script>
    export default {
        name: "NtFooter"
    }
</script>
