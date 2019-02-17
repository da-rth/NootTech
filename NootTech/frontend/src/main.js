import Vue from 'vue'
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'
import 'babel-polyfill'
import router from './router'
import store from './store'
import * as backendAPI from './api.js'
import VuePaginate from 'vue-paginate'

// Import CSS assets
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
Vue.use(VuePaginate);
Vue.prototype.$api = backendAPI;
Vue.prototype.$site_url = 'http://localhost:8080/';
Vue.prototype.$subdomain_url = ".noot.tech";
Vue.prototype.$subdomain_enabled = false;

// load BootstrapVue
Vue.use(BootstrapVue);

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
});
