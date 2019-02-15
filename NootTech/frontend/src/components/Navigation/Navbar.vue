<template>
    <div>
        <b-navbar toggleable="lg" variant="dark" type="dark">
            <b-navbar-toggle target="nav_collapse" />
            <b-collapse is-nav id="nav_collapse">
                <b-navbar-nav>
                  <b-nav-item><router-link to="/about">About</router-link></b-nav-item>
                    <b-nav-item><router-link to="/tos">Terms of Service</router-link></b-nav-item>
                </b-navbar-nav>
                <!-- Keep this centered -->
                <b-navbar-nav class="mx-auto">
                  <b-navbar-brand><router-link to="/">{{ brandName }}</router-link></b-navbar-brand>
                </b-navbar-nav>
                <b-navbar-nav class="ml-auto">
                    <b-nav-item><router-link to="/login">Login</router-link></b-nav-item>
                    <b-nav-item><router-link to="/register">Register</router-link></b-nav-item>
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
                isLoggedIn: "False",
                users: [],
                text: "To Load"
            };
        },

        created() {
            console.log(this.$api_url+"/list-users");
            axios.get(this.$api_url+"/list-users")
                .then(response => {
                    console.log(response);
                    this.users = response.data
                })
                .catch(e => {
                this.errors.push(e)
            })
            console.log(this.$api_url+"/ToS");
        },

        components: {NtPopup}

    }
</script>
<style scoped>
  .navbar.bg-dark {
    background-color: #242424 !important;
  }
  .navbar a {
    color: #8f8f8f;
  }
  .navbar a:hover {
    color: #d1d1d1;
    text-decoration: none;
  }
</style>
