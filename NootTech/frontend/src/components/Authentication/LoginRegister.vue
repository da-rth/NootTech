<template>
  <div>

    <b-alert class="auth-error" show variant="danger" dismissible v-if="formatted_error">
      <p v-html="formatted_error"></p>
    </b-alert>

    <div class="container-login" :class="{'registration-page': currentTab}" :style="{backgroundColor: getColour()}">

      <b-card no-body>
        <b-tabs pills card @input="updateTab">

          <b-tab ref="loginTab" title="Login" active>
            <b-form @submit.prevent="login">
              <b-form-group id="usernameFormGroup" label="Your username" label-for="usernameLoginField">
                <b-form-input
                  id="usernameLoginField" type="text" placeholder="Username" v-model="login_credentials.username" required />
              </b-form-group>
              <b-form-group id="passwordFormGroup" label="Your password" label-for="passwordFormGroup">
                <b-form-input id="passwordLoginField" type="password" v-model="login_credentials.password" required/>
              </b-form-group>
              <b-button type="submit" variant="primary">Log in</b-button>
            </b-form>
          </b-tab>

          <b-tab title="Register">
            <b-form @submit.prevent="register">
              <b-form-group
                id="usernameFormGroup"
                label="Insert your username"
                description="This will uniquely distinguish you"
                label-for="usernameSigninField"
                required>


                <b-form-input
                  id="usernameSigninField"
                  type="text"
                  placeholder="Username"
                  v-model="register_credentials.username"
                  required
                />
              </b-form-group>
              <b-form-group
                id="emailFormGroup"
                label="Insert your email"
                label-for="emailSigninField"
                required>

                <b-form-input
                  id="emailSigninField"
                  type="email"
                  placeholder="user@example.com"
                  v-model="register_credentials.email"
                  required
                />
              </b-form-group>
              <b-form-group
                id="passwordSigninFormGroup"
                label="Insert your password"
                label-for="emailSigninField"
                required
                >

                <b-form-input
                  id="emailSigninField"
                  type="password"
                  placeholder="user@example.com"
                  v-model="register_credentials.password"
                  required
                />
              </b-form-group>
              <b-form-group
                id="colourForGroup"
                label="Insert your colour"
                label-for="colourSigninField">

                <slider id="colourSigninField" v-model="register_credentials.colour" />
             </b-form-group>
              <b-button type="submit" variant="primary">Register</b-button>
            </b-form>
          </b-tab>
        </b-tabs>
      </b-card>
    </div>
  </div>
</template>

<script>
import * as types from '../../store/mutation-types'

import {Slider} from 'vue-color';
import {TinyColor} from '@ctrl/tinycolor';

let colour = "#00cccc";

export default {
  components: {Slider},
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
        colour: '#00cccc'
      },
      error: null,
      formatted_error: null,
      creationIsSuccessful: false,
      currentTab: 0
    }
  },
  methods: {
    getColour() {
      var colour = this.register_credentials.colour
      if(typeof (colour) !== "string")
        colour = colour.hex
      return colour
    },
    updateTab(tabIndex) {
      this.currentTab = tabIndex
    },
    renderErrors (e) {
        console.log(e);
        this.formatted_error = '<strong>Whoops!</strong> Something went wrong...<br/>';

          for (var key in e) {
              if (Array.isArray(e[key])) {
                  for (var i =0; i < e[key].length; i++) {
                      this.formatted_error += `<p>- ${e[key][i]}</p>`
                  }
              } else {
                  this.formatted_error += `<p>- ${e[key]}</p>`
              }
          }
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
      let params = {
        credentials: this.register_credentials,
        redirect: decodeURIComponent(this.$route.query.redirect || '/')
      };
      // get the colour as hex
      params.credentials.colour = this.getColour()
      this.$store.dispatch(types.REGISTER, params).then(response => {
        console.log("User created!")
      }).catch(errors => {
        this.error = errors
        console.log("Failed to create user")
        this.renderErrors(errors.response.data)
      });
    }
  }
}
</script>


<style scoped>

.container-login {
  width: 320px;
  margin: 0 auto;
  margin-bottom: 40px;
  padding: 20px;
  background-color: rgba(0,0,0,0.2);
  border: 1px solid rgba(0,0,0,0.4);
  border-radius: 5px;
  -webkit-box-shadow: 0px 0px 36px 3px rgba(0,0,0,0.7);
  -moz-box-shadow: 0px 0px 36px 3px rgba(0,0,0,0.7);
  box-shadow: 0px 0px 36px 3px rgba(0,0,0,0.7);
}

.registration-page {
  width: 500px;
}

.auth-error {
  padding-bottom: 0;
  width: 34%;
  margin: 0 auto;
  background: rgba(0,0,0,0.3);
  color: #ffffffbb;
  border: 1px solid rgba(255,0,0,0.6);
  margin-top: 40px;
  margin-bottom: 60px;
  transition: all 0.2s ease-in-out;
}
.btn-login {
  width: 100%;
  padding: 8px;
  background-color: rgba(0,0,0,0.2);
  border: 1px solid rgba(120,120,120,0.3);
  color: #ffffffdd;
}
.btn-login:hover {
  border-color: #00cccc;
  color: white;
  cursor: pointer;
}

.nav-tabs .nav-link.active,
.nav-tabs .nav-item.show .nav-link {
  color: #00cccc;
  opacity: 0.9;
  background: transparent;
}

.nav-tabs .nav-link.active:hover,
.nav-tabs .nav-item.show .nav-link:hover {
  opacity: 1;
}

</style>
