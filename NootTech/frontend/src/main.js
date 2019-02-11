import Vue from 'vue'
import App from './App.vue'

Vue.prototype.$api_url = 'http://localhost:8000/api';
Vue.prototype.$subdomain_url = ".noot.tech";
Vue.prototype.$subdomain_enabled = false;

new Vue({
  el: '#app',
  render: h => h(App)
});
