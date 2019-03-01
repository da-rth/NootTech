<template>
  <div>
    <b-navbar
    toggleable="lg"
    variant="dark"
    type="dark"
    :style="{borderBottom: `1px solid ${$root.colour}`}">

      <notifications group="FileUpload" />

      <b-navbar-toggle target="nav_collapse"/>
      <b-collapse is-nav id="nav_collapse">

        <template v-if="$store.state.user != null">
          <b-button class="settings-modal-btn" v-if="$store.state.user">
              <font-awesome-icon icon="user-ninja"/>&nbsp; {{ $store.state.user.username }}
          </b-button>
          &nbsp;
          <b-button class="favs-modal-btn">
              <font-awesome-icon icon="bookmark"/>&nbsp; Favourites
          </b-button>
        </template>

        <b-navbar-nav v-else>
          <b-nav-item>
            <router-link to="/about">
            <font-awesome-icon icon="info-circle"/>&nbsp; About
            </router-link>
          </b-nav-item>
        </b-navbar-nav>

          &nbsp;
          <router-link to="/how-to">
            <font-awesome-icon icon="question-circle"/>
            &nbsp;How to...
          </router-link>

        <!-- Keep this centered -->
        <b-navbar-brand>

          <router-link class="navbar-brand" to="/">

            <template v-if="$root.sharelinkName">
              {{ $root.sharelinkName }}.<span v-bind:style="{color: $root.colour}">Noot</span>.Tech
            </template>

            <template v-else>
              Noot<span v-bind:style="{color: $root.colour}" class="tech">Tech</span>
            </template>

          </router-link>
        </b-navbar-brand>

        <b-navbar-nav class="ml-auto" v-if="$store.state.user">
          <b-input-group class="filebar-uploadkey" v-if="showUploadKey">
            <b-form-input class="key-field" v-bind:value="$store.state.settings.upload_key" readonly/>
            <b-input-group-append>
              <b-button>Copy</b-button>
            </b-input-group-append>
            &nbsp;&nbsp;
          </b-input-group>

          <b-nav-item>
            <a @click="$store.commit('CHANGE_MODAL', 'upload')">

              <font-awesome-icon icon="upload"/>&nbsp; Upload
            </a>
          </b-nav-item>

          <b-nav-item>
            <a v-on:click="showUploadKey = !showUploadKey" name="check-button">
              <font-awesome-icon icon="eye-slash" v-if="showUploadKey"/>
              <font-awesome-icon icon="eye" v-else/>&nbsp;
              {{ showUploadKey ? "&nbsp;Hide Key" : "Show Key" }}
            </a>
            &nbsp;&nbsp;
            <router-link to="/logout">
              <font-awesome-icon :icon="['fas', 'sign-out-alt']"/> Logout
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
  import NtUploadModal from '../Modals/UploadModal'

  export default {
    name: 'NtNavbar',
    data() {
      return {
        brandName: "NootTech",
        showUploadKey: false
      };
    },
    components: {NtPopup, NtUploadModal},
  }

</script>
<style>
  .navbar.bg-dark {
    background-color: #202020 !important;
    border-bottom: 1px solid #121212;
    transition: 0.5s ease-in-out;
  }

  .tech {
    transition: 0.5s ease-in-out;
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
  .user-dropdown button {
    color: red;
  }
  .favs-modal-btn,
  .settings-modal-btn {
    padding: 0px 10px;
    border: none;
    background: transparent;
    color: #909090;
  }
  .favs-modal-btn:hover,
  .settings-modal-btn:hover {
    color: #FFFFFF;
  }
</style>
