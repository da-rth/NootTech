<template>
  <div>

    <div class="container-login" :class="{'registration-page': currentTab}" :style="{backgroundColor: getColour()}">

      <b-card no-body>
        <b-tabs pills card @input="updateTab">

          <b-tab ref="loginTab" title="Login" active>
            <b-form @submit.prevent="login">
                <b-form-input id="usernameLoginField" type="text" placeholder="Username" class="log-reg-field" v-model="login_credentials.username" required />
                <b-form-input id="passwordLoginField" class="log-reg-field"  placeholder="Password" type="password" v-model="login_credentials.password" required/>
              <b-button type="submit" variant="primary" class="auth-button" :style="{backgroundColor: getColour()}">Log in</b-button>
            </b-form>
          </b-tab>

          <b-tab title="Register">
            <b-form @submit.prevent="register">
                <b-form-input
                  id="usernameSigninField"
                  type="text"
                  class="log-reg-field"
                  placeholder="Enter a username!"
                  v-model="register_credentials.username"
                  required
                />
                <b-form-input
                  id="emailSigninField"
                  type="email"
                  class="log-reg-field"
                  placeholder="Enter a your email address"
                  v-model="register_credentials.email"
                  required
                />

                <b-form-input
                  id="emailSignupField"
                  type="password"
                  class="log-reg-field"
                  placeholder="Enter a secure password"
                  v-model="register_credentials.password"
                  required
                />

                <b-form-input
                  id="emailSignupField"
                  type="password"
                  class="log-reg-field"
                  placeholder="Confirm your password"
                  v-model="register_credentials.confirm_password"
                  required
                />

                <password v-model="register_credentials.password" :strength-meter-only="true"/>

              <b-form-group
                id="colourForGroup"
                label="Pick a colour!"
                label-for="colourSigninField"
              >

                <slider id="colourSigninField" v-model="register_credentials.colour" />
              </b-form-group>
              <b-button type="submit" variant="primary" class="auth-button" :style="{backgroundColor: getColour()}">Register</b-button>
            </b-form>
          </b-tab>
        </b-tabs>
      </b-card>
    </div>
  </div>
</template>

<script>
import * as types from '../../store/mutation-types'
import Password from 'vue-password-strength-meter'

import {Slider} from 'vue-color';

export default {
  components: {Slider, Password},
  data () {
    return {
      login_credentials: {
        username: '',
        password: ''
      },
      register_credentials: {
        username: '',
        email: '',
        password: '',
        confirm_password: '',
        colour: this.$root.default_colour
      },
      error: null,
      formatted_error: null,
      creationIsSuccessful: false,
      currentTab: 0,
      password: null,
    }
  },
  methods: {
    getColour() {
      var colour = this.register_credentials.colour
      if(typeof (colour) !== "string")
        colour = colour.hex;
        this.$root.colour = colour;
      return colour
    },
    updateTab(tabIndex) {
      this.currentTab = tabIndex
    },
    renderErrors (e) {
        console.log(e);
        this.formatted_error = ''
        let title = '<strong>Whoops!</strong> Something went wrong...';

          for (var key in e) {
              if (Array.isArray(e[key])) {
                  for (var i =0; i < e[key].length; i++) {
                      this.formatted_error += `<p>- ${e[key][i]}</p>`
                  }
              } else {
                  this.formatted_error += `<p>- ${e[key]}</p>`
              }
          }
        this.$notify({
          group: 'Global',
          title: title,
          text: this.formatted_error,
          position: 'top right',
          type: "error",
          duration: 5000,
        });
    },
    async login(evt) {
      let params = {
          credentials: this.login_credentials,
          redirect: decodeURIComponent(this.$route.query.redirect || '/')
      };
      this.$store.dispatch(types.LOGIN, params).then(response => {}).catch(errors =>  {
        this.error = errors
        this.renderErrors(errors.response.data)})
    },

    async register(evt) {
      if (this.register_credentials.password != this.register_credentials.confirm_password) {
        this.formatted_error = "<strong>Whoops!</strong> Something went wrong...<br/> - Your passwords don't match!";
        return
      }

      let params = {
        credentials: this.register_credentials,
        redirect: decodeURIComponent(this.$route.query.redirect || '/')
      };
      // get the colour as hex
      params.credentials.colour = this.getColour()
      try {
        this.$store.dispatch(types.REGISTER, params)
      } catch(errors) {
        this.error = errors
        console.log("Failed to create user")
        this.renderErrors(errors.response.data)
      }
    }
  },

  mounted() {
    if (this.$store.state.user != null) {
      console.log("User already authenticated, redirecting...")
      this.$router.push("/");
    }
  },
}
</script>

<style>
.vc-slider-swatch:last-child {
  opacity: 0;
  display: none !important;
}

.nav-link.active {
  background-color: #403f3f !important;
}

.nav-link {
  color: #dadada !important;
}
</style>
<style scoped>

.container-login {
  margin: 17vh auto;
  max-width: 360px;
  padding: 1px;
  background-color: rgba(0,0,0,0.2);
  border: 1px solid rgba(0,0,0,0.4);
  border-radius: 5px;
  -webkit-box-shadow: 0px 0px 36px 3px rgba(0,0,0,0.7);
  -moz-box-shadow: 0px 0px 36px 3px rgba(0,0,0,0.7);
  box-shadow: 0px 0px 36px 3px rgba(0,0,0,0.7);
}

.card {
  background-color: #191919;
  color: #bababa;
}

.auth-error {
  position: absolute;
  left: 0; right: 0;
  top: 10vh;
  padding-bottom: 0;
  margin: 0 auto;
  max-width: 340px;
  background: #191919;
  color: #ffffffbb;
  border: 1px solid rgba(255,0,0,0.6);
  transition: all 0.2s ease-in-out;
}


.nav-tabs .nav-link.active,
.nav-tabs .nav-item.show .nav-link {
  color: #00cccc;
  opacity: 0.9;
  background: transparent;
}
.vc-slider-swatch:last-child {
  opacity: 0;
  display: none !important;
}
.nav-tabs .nav-link.active:hover,
.nav-tabs .nav-item.show .nav-link:hover {
  opacity: 1;
}
.auth-button {
  border: none;
  -webkit-transition: none;
  -moz-transition: none;
  -ms-transition: none;
  -o-transition: none;
  transition: none;
  width: 100%;
}

  .log-reg-field {
    margin: 20px 0px;
  }

  .card-body {
    margin-top: -20px;
  }

  .tab-content:focus, .tab-pane:focus {
    outline: none !important;
  }
.nav-pills .nav-link.active,
.nav-pills .show > .nav-link a {
    color: #fff !important;
    background-color: #3d3d !important;
}

.vc-slider {
  width: auto !important;
}
</style>
