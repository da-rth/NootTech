<template>
  <div>

    <b-alert class="auth-error" show variant="danger" dismissible v-if="formatted_error">
      <p v-html="formatted_error"></p>
    </b-alert>

    <div class="container-login">

      <b-card no-body>
        <b-tabs pills card>

          <b-tab ref="loginTab" title="Login" active>
            <div class="form-group"><input type="text" class="form-control" placeholder="Username" v-model="login_credentials.username" required></div>
            <div class="form-group"><input type="password" class="form-control" placeholder="Password" v-model="login_credentials.password" required></div>
            <button class="btn btn-login" @click="submit('login')">Login</button>
          </b-tab>

          <b-tab title="Register">
            <div class="form-group"><input type="text" class="form-control" placeholder="Username" v-model="register_credentials.username" required></div>
            <div class="form-group"><input type="email" class="form-control" placeholder="Email" v-model="register_credentials.email" required></div>
            <div class="form-group"><input type="password" class="form-control" placeholder="Password" v-model="register_credentials.password" required></div>
            <div class="form-group"><input type="text" class="form-control" placeholder="Pick a colour" value="#00CCCC" v-model="register_credentials.colour"></div>
            <button class="btn btn-login" @click="submit('register')">Register</button>
          </b-tab>
        </b-tabs>
      </b-card>

    </div>

  </div>
</template>

<script>
import * as types from '../../store/mutation-types'

export default {
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
        colour: ''
      },
      error: null,
      formatted_error: null,
      creationIsSuccessful: false
    }
  },
  methods: {
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
    async submit (type) {
        this.formatted_error = null;
        if (type === "login") {
            let params = {
                credentials: this.login_credentials,
                redirect: decodeURIComponent(this.$route.query.redirect || '/')
            };
            this.$store.dispatch(types.LOGIN, params).then(response => { }).catch(errors => {
              console.log("Failed to login")
              this.error = errors
              this.renderErrors(errors.response.data)})
        }
        if (type === "register") {
            let params = {
                credentials: this.register_credentials,
                redirect: decodeURIComponent(this.$route.query.redirect || '/')
            };
            this.$store.dispatch(types.REGISTER, params).then(response => {
              console.log("User created!")
            }).catch(errors => {
              this.error = errors
              console.log("Failed to create user")
              this.renderErrors(errors.response.data)})
        }
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
