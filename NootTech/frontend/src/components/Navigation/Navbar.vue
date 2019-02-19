<template>
    <div>
        <b-navbar toggleable="lg" variant="dark" type="dark">
            <b-navbar-toggle target="nav_collapse" />
            <b-collapse is-nav id="nav_collapse">

                <b-dropdown id="userdropdown" v-bind:text="$store.state.user.username" v-if="$store.state.user.authenticated">
                  <b-dropdown-item href="#">Favourites</b-dropdown-item>
                  <b-dropdown-item href="#">Upload History</b-dropdown-item>
                  <b-dropdown-item href="#">Settings</b-dropdown-item>
                </b-dropdown>

                <b-navbar-nav v-else>
                  <b-nav-item><router-link to="/about">About</router-link></b-nav-item>
                  <b-nav-item><router-link to="/tos">Terms of Service</router-link></b-nav-item>
                </b-navbar-nav>

                  <!-- Keep this centered -->
                  <b-navbar-nav class="mx-auto">
                    <b-navbar-brand><router-link class="navbar-brand" to="/">noot.<span class="brand-right">tech</span></router-link></b-navbar-brand>
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
    import axios from 'axios'

    export default {
        name: 'NtNavbar',
        data: function() {
            return {
                brandName: "NootTech",
                text: "To Load"
            };
        },


    }
</script>
<style scoped>
  .navbar.bg-dark {
    background-color: #202020 !important;
    border-bottom: 1px solid #00cccc;
  }

  .navbar.bg-dark .navbar-brand {
    position: absolute;
    left: 50%;
    top: 2px;
    transform: translateX(-50%);
    font-size: 24px;
    border-bottom: 1px solid black;
  }

  .brand-right {
    color: #00cccc;
  }
  .navbar a {
    color: #8f8f8f;
  }
  .navbar a:hover {
    color: #d1d1d1;
    text-decoration: none;
  }

  .btn .btn-secondary .dropdown-toggle {
    background-color: transparent !important;
    border: none;
    color: #969696;
  }
</style>
