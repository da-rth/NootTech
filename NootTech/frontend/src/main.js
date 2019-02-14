import Vue from 'vue'
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'
import 'babel-polyfill'


Vue.prototype.$api_url = 'http://localhost:8000/api';
Vue.prototype.$subdomain_url = ".noot.tech";
Vue.prototype.$subdomain_enabled = false;

// load BootstrapVue
Vue.use(BootstrapVue);

new Vue({
  el: '#app',
  render: h => h(App)
});
