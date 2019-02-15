<template>
    <div>
        <b-navbar toggleable="lg" variant="dark" type="dark">
            <b-navbar-toggle target="nav_collapse" />
            <b-collapse is-nav id="nav_collapse">
                <b-navbar-nav>
                    <b-link @click="$refs.tos_modal.showModal()">Terms of Service</b-link>
                    <nt-popup title="Terms of service" ref="tos_modal" id="tos">
                        {{text}}
                    </nt-popup>
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
