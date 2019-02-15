<template>
    <div>
        <b-navbar toggleable="lg" variant="dark" type="dark">
            <b-navbar-toggle target="nav_collapse" />
            <b-collapse is-nav id="nav_collapse">

                <b-dropdown v-bind:text="$store.state.user.username" v-if="$store.state.user.authenticated">
                  <b-dropdown-item href="#">An item</b-dropdown-item>
                  <b-dropdown-item href="#">Another item</b-dropdown-item>
                </b-dropdown>

                <b-navbar-nav v-else>
                  <b-nav-item><router-link to="/about">About</router-link></b-nav-item>
                  <b-nav-item><router-link to="/tos">Terms of Service</router-link></b-nav-item>
                </b-navbar-nav>

                  <!-- Keep this centered -->
                  <b-navbar-nav class="mx-auto">
                    <b-navbar-brand><router-link to="/">{{ brandName }}</router-link></b-navbar-brand>
                  </b-navbar-nav>

                  <b-navbar-nav class="ml-auto" v-if="$store.state.user.authenticated">
                    <b-nav-item><router-link to="/logout">Logout</router-link></b-nav-item>
                  </b-navbar-nav>

                  <b-navbar-nav class="ml-auto" v-else>
                    <b-nav-item><router-link to="/login">Login / Register</router-link></b-nav-item>

                </b-navbar-nav>
            </b-collapse>

        </b-navbar>
    </div>
</template>
<script>
    import NtPopup from '../Utils/Popup.vue'
    import axios from 'axios'

    export default {
        name: 'NtNavbar',
        data: function() {
            return {
                brandName: "NootTech",
                text: "To Load"
            };
        },

        components: {NtPopup}

    }
</script>
<style scoped>
  .navbar.bg-dark {
    background-color: #202020 !important;
  }
  .navbar a {
    color: #8f8f8f;
  }
  .navbar a:hover {
    color: #d1d1d1;
    text-decoration: none;
  }
</style>
