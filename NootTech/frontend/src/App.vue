<template>
  <div id="NTapp">
    <notifications position="top right" class="nt-notif" group="Global" />
    <nt-modal/>
    <nt-navbar></nt-navbar>
    <router-view/>
    <nt-footer></nt-footer>
  </div>
</template>

<script>
  import NtNavbar from './components/Navigation/Navbar.vue';
  import NtFooter from './components/Navigation/Footer.vue';
  import NtModal from './components/Modals/Modal.vue';
  import decode from 'jwt-decode';

  export default {
    name: 'app',
    data () {
      return {
        title: "NootTech",
        domain: 'noot.tech'
      }
    },
    computed: {
      token () {
        return this.$store.state.token
      },
      user () {
        return this.$store.state.user
      },
    },
    components: {
      NtNavbar, NtFooter, NtModal
    },

    methods: {
      getTokenExpirationDate: function (encodedToken) {
        const token = decode(encodedToken);
        if (!token.exp) {
          return null;
        } else {
          const date = new Date(0);
          date.setUTCSeconds(token.exp);
          return date;
        }
      },

      isTokenAlmostExpired: function (token) {
        const TokenNearExpirationDate = this.getTokenExpirationDate(token);
        TokenNearExpirationDate.setMinutes(TokenNearExpirationDate.getMinutes() - 6);
        return TokenNearExpirationDate < new Date();
      },

      checkToken: function () {
        if (this.user) {
          if (this.token && this.isTokenAlmostExpired(this.token)) {
            console.log('Token about to expire, refreshing!');
            this.$store.dispatch('REFRESH', {token: this.token});
          }
        }
      }
    },
    async beforeMount () {
      
      if (this.token) {
        this.$store.dispatch('VERIFY', {token: this.token});
        this.checkToken()
      }
      document.title = this.title;
    },
  }
</script>

<style>

.vue-notification {
  margin: -3px 5px 5px;
  font-size: 14px;
  color: #dadada;
  background: #242424 !important;
  border: 1px solid rgba(255,255,255,0.3) !important;
}

.nt-notif.success {
    background: transparent;
    border-left-color: transparent;
}
</style>
