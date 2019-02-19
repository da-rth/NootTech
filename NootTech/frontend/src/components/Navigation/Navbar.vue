<template>
  <div>
    <b-navbar toggleable="lg" variant="dark" type="dark">
      <b-navbar-toggle target="nav_collapse"/>
      <b-collapse is-nav id="nav_collapse">

        <template v-if="$store.state.user.authenticated">

          <b-dropdown v-bind:text="$store.state.user.username">
            <b-dropdown-item>Favourites</b-dropdown-item>
            <b-dropdown-item>Upload History</b-dropdown-item>
            <b-dropdown-item>Settings</b-dropdown-item>
          </b-dropdown>
           &nbsp;&nbsp;
          <router-link to="/how-to">
            <font-awesome-icon :icon="['fas', 'cloud']"/>
            How to...
          </router-link>
        </template>

        <b-navbar-nav v-else>
          <b-nav-item>
            <router-link to="/about">About</router-link>
          </b-nav-item>
        </b-navbar-nav>

        <!-- Keep this centered -->
        <b-navbar-brand>
          <router-link class="navbar-brand" to="/">noot.<span class="brand-right">tech</span></router-link>
        </b-navbar-brand>

        <b-navbar-nav class="ml-auto" v-if="$store.state.user.authenticated">

          <b-input-group class="filebar-uploadkey" v-if="showUploadKey">
            <b-form-input class="key-field" v-bind:value="$parent.settings.upload_key" readonly/>
            <b-input-group-append>
              <b-button>Copy</b-button>
            </b-input-group-append>
          </b-input-group>

          <b-nav-item>
            <a v-on:click="showUploadKey = !showUploadKey" name="check-button">
              &nbsp;
              <font-awesome-icon :icon="['fas', 'eye-slash']" v-if="showUploadKey"/>
              <font-awesome-icon :icon="['fas', 'eye']" v-else/>
              {{ showUploadKey ? "&nbsp;Hide Key" : "Show Key" }}
            </a>
            &nbsp;
            <router-link to="/logout">
              <font-awesome-icon :icon="['fas', 'sign-out-alt']"/> &nbsp;Logout
            </router-link>
          </b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto" v-else>
          <b-nav-item>
            <router-link to="/login">
              <font-awesome-icon :icon="['fas', 'sign-in-alt']"/> &nbsp;Login / Register
            </router-link>
          </b-nav-item>

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
    data: function () {
      return {
        brandName: "NootTech",
        text: "To Load",
        showUploadKey: false
      };
    },

    components: {NtPopup}

  }
</script>
<style scoped>
  .navbar.bg-dark {
    background-color: #202020 !important;
    border-bottom: 1px solid #121212;
  }

  .navbar.bg-dark .navbar-brand {
    position: absolute;
    left: 50%;
    top: 2px;
    transform: translateX(-50%);
    font-size: 24px;
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

  .filebar-uploadkey {
    margin-top: 4px;
    width: 230px;
    text-align: center;
  }

  .filebar-uploadkey .btn,
  .filebar-uploadkey .input-group-text,
  .filebar-uploadkey .key-field {
    font-size: 12px;
  }

  .filebar-uploadkey .input-group-text,
  .filebar-uploadkey .key-field {
    color: #242424;
  }

  .filebar-uploadkey .btn {
    height: 32px;
  }
</style>
