import Vue from 'vue'
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'
import 'babel-polyfill'
import router from './router'
import store from './store'
import * as backendAPI from './api.js'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
 
library.add(fas)

Vue.component('font-awesome-icon', FontAwesomeIcon);

Vue.config.productionTip = false;

// Import CSS assets
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
Vue.prototype.$api = backendAPI;
Vue.prototype.$site_url = 'http://localhost:8080/';
Vue.prototype.$subdomain_url = ".noot.tech";
Vue.prototype.$subdomain_enabled = false;
Vue.prototype.$userColour = "#00CCCC";

// load BootstrapVue
// todo: load the single components instead
Vue.use(BootstrapVue);

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
});

Vue.mixin({
  data() {
    return {
      companyName: "NootTech"
    }
  },
})