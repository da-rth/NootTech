<template>
    <div>
        <b-navbar toggleable="lg" variant="dark" type="dark">
            <b-navbar-toggle target="nav_collapse" />
            <b-collapse is-nav id="nav_collapse">
                <b-navbar-nav>
                    <b-nav-item-dropdown text="Pick an user" v-if="users">
                        <b-dropdown-item v-for="user in users" :key="user.id">{{user.username}}</b-dropdown-item>
                    </b-nav-item-dropdown>
                    <b-link v-else href="#TOS">User listing not available</b-link>
                </b-navbar-nav>
                <b-navbar-nav>
                    <b-nav-item href="/TOS" size="md">Terms of Service</b-nav-item>
                </b-navbar-nav>
                <!-- Keep this centered -->
                <b-navbar-nav class="mx-auto">
                    <b-navbar-brand href="#">{{ brandName }}</b-navbar-brand>
                </b-navbar-nav>
                <b-navbar-nav class="ml-auto">
                    <b-nav-item>Login</b-nav-item>
                    <b-nav-item>Register</b-nav-item>
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
                isLoggedIn: "False",
                users: []
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
        },

    }
</script>
