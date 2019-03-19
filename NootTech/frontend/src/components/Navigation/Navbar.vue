<template>
  <div>
    <notifications group="CopyKey" />

    <b-navbar
    toggleable="lg"
    variant="dark"
    type="dark"
    :style="{borderBottom: `1px solid ${$root.colour}`}">

      <!-- Keep this centered -->
      <b-navbar-brand>
        <router-link to="/">
          <template v-if="$root.sharelinkName">
            {{ $root.sharelinkName }}.<span v-bind:style="{color: $root.colour}">Noot</span>.Tech
          </template>
          <template v-else>
            Noot<span v-bind:style="{color: $root.colour}" class="tech">Tech</span>
          </template>
        </router-link>
      </b-navbar-brand>
      

      <notifications group="FileUpload" />

      <b-navbar-nav v-if="$store.state.user != null">
        <b-nav-item>
          <b-button class="navbar-btn" v-if="$store.state.user" @click="raiseEvent('settingsModal')">
              <font-awesome-icon icon="user-ninja"/>&nbsp;&nbsp;&nbsp; {{ $store.state.user.username }}
          </b-button>
        </b-nav-item>
      </b-navbar-nav>

      <b-navbar-toggle class="float-xs-right" target="nav_collapse"/>

      <b-collapse is-nav id="nav_collapse">

        <b-navbar-nav v-if="$store.state.user != null">
          
          <b-nav-item>
            <b-button class="navbar-btn" @click="raiseEvent('favouriteModal')">
                <font-awesome-icon icon="bookmark"/>&nbsp;&nbsp;&nbsp; Favourites
            </b-button>
          </b-nav-item>
          <b-nav-item>
            <router-link to="/admin">
              <b-button class="navbar-btn">
                <font-awesome-icon icon="tachometer-alt"/> &nbsp;Admin panel
              </b-button>
            </router-link>
          </b-nav-item>
        </b-navbar-nav>


        <b-navbar-nav v-else>

          <b-nav-item>
            <router-link to="/about">
            <font-awesome-icon icon="info-circle"/>&nbsp; About
            </router-link>
          </b-nav-item>
          
          <b-nav-item>
            <router-link to="/how-to">
              <font-awesome-icon icon="question-circle"/>
              &nbsp;How to...
            </router-link>
          </b-nav-item>
        </b-navbar-nav>





        <b-navbar-nav class="ml-auto" v-if="$store.state.user">
          <b-nav-item>
            <b-button class="navbar-btn" @click="raiseEvent('uploadFile')">
              <font-awesome-icon icon="upload"/>&nbsp;&nbsp; Upload
            </b-button>
          </b-nav-item>

          <b-nav-item>
            <router-link to="/logout">
            <b-button class="navbar-btn">
              <font-awesome-icon :icon="['fas', 'sign-out-alt']"/> &nbsp;Logout
            </b-button>
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
  import EventBus from '../../event-bus.js';

  export default {
    name: 'NtNavbar',
    data() {
      return {
        brandName: "NootTech",
        showUploadKey: false
      };
    },
    methods: {
      copyUploadKey () {
        let testingCodeToCopy = document.querySelector('#uploadKey')
        testingCodeToCopy.setAttribute('type', 'text')
        testingCodeToCopy.select()
        try {
          var successful = document.execCommand('copy');
          this.showUploadKey = false;
          this.$notify({
            group: 'CopyKey',
            title: `Copied Upload Key to clipboard!`,
            text: 'Remember to keep it safe!',
          });
        } catch (err) {
          this.$notify({
            group: 'CopyKey',
            title: 'Oh no! We couldn\'t copy the upload key',
            text: 'Try using CTRL+C! Sorry about that...',
          });
        }
        testingCodeToCopy.setAttribute('type', 'hidden')
        window.getSelection().removeAllRanges()
      },
      raiseEvent(eventType) {
        EventBus.$emit(eventType);
      },
   },
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

  .filebar-uploadkey {
    margin: -5px;
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

  input#uploadKey {
    background-color: #2a2a2a;
    color: white;
    border: 1px solid #181818;
  }

  .navbar-btn {
    margin: -10px !important;
    padding: 10px 10px !important;
    border: none !important;
    background: transparent !important;
    color: #909090 !important;
    transition: 0.3s ease-in-out !important;
  }
  .navbar-btn:hover {
    color: #FFFFFF !important;
  }

  .navbar-btn:focus {
    box-shadow: none !important;
  }

  .navbar-dark .navbar-toggler {
    border-radius: 0px;
    border: none;
  }
  .navbar-dark .navbar-toggler:focus {
    outline: none;
  }

  .copy-btn {
    background-color: #242424 !important;
    border: 1px solid #181818 !important;
  }
</style>
