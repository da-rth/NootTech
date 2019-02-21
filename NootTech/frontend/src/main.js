import Vue from 'vue'
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'
import 'babel-polyfill'
import router from './router'
import store from './store'
import * as backendAPI from './api.js'
import VuePaginate from 'vue-paginate'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import './assets/css/main.css'
import VueVideoPlayer from 'vue-video-player'
import Notifications from 'vue-notification'

// CSS Imports
import 'video.js/dist/video-js.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

library.add(fas)

Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.config.productionTip = false;

// Import CSS assets


Vue.use(VuePaginate);
Vue.use(VueVideoPlayer);
Vue.use(Notifications);
Vue.use(BootstrapVue);

Vue.prototype.$api = backendAPI;
Vue.prototype.$site_url = 'http://localhost:8000';
Vue.prototype.$subdomain_enabled = false;

// load BootstrapVue

Vue.directive('highlightjs', {
    deep: true,
    bind: function (el, binding) {
        let targets = el.querySelectorAll('code');
        targets.forEach((target) => {
            if (binding.value) {
                target.textContent = binding.value
            }
            hljs.highlightBlock(target)
        })
    },
    componentUpdated: function (el, binding) {
        let targets = el.querySelectorAll('code');
        targets.forEach((target) => {
            if (binding.value) {
                target.textContent = binding.value;
                hljs.highlightBlock(target)
            }
        })
    }
});

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
});
