<template>
  <div id="NTapp">
    <nt-navbar></nt-navbar>
    <router-view/>
    <nt-footer></nt-footer>
  </div>
</template>

<script>
  import NtNavbar from './components/Navigation/Navbar.vue'
  import NtFooter from './components/Navigation/Footer.vue'
import decode from 'jwt-decode';

  export default {
    name: 'app',
    data () {
      return {
        settings: null,
        files: null,
        isLoading: false,
        subdomain: false,
        domain: 'noot.tech'
      }
    },
    computed: {
      token () {
        return this.$store.state.token
      },
      user () {
        return this.$store.state.user
      }
    },
    components: {
      NtNavbar, NtFooter
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
        if (this.user.authenticated) {
          if (this.token && this.isTokenAlmostExpired(this.token)) {
            console.log('Token about to expire, refreshing!');
            this.$store.dispatch('REFRESH', {token: this.token});
          }
        }
      }
    },
    async beforeMount () {
      this.$store.dispatch('VERIFY', {token: this.token});
      this.checkToken()
      if (this.token) {
        this.settings = await this.$api.GetSettings();
      }
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
