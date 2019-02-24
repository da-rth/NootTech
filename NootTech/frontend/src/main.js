import Vue from 'vue'
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'
import 'babel-polyfill'
import router from './router'
import store from './store'
import * as backendAPI from './api.js'
import * as config from './config.js'
import VuePaginate from 'vue-paginate'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import './assets/css/main.css'
import VueVideoPlayer from 'vue-video-player'
import Notifications from 'vue-notification'

// CSS Imports
import 'video.js/dist/video-js.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// register FontAwesome fonts
library.add(fas);
library.add(far);

Vue.component('font-awesome-icon', FontAwesomeIcon);

// Enable a bunch of Vue plugins
Vue.use(VuePaginate);
Vue.use(VueVideoPlayer);
Vue.use(Notifications);

// load BootstrapVue
Vue.use(BootstrapVue);

Vue.prototype.$api = backendAPI;
Vue.prototype.$site_url = config.SITE_URL;
Vue.prototype.$backend_url = config.BACKEND_URL;
Vue.prototype.$subdomain_enabled = config.ENABLE_SUBDOMAINS;
Vue.prototype.$default_colour = config.DEFAULT_HIGHLIGHT;

Vue.mixin({
  data: function () {
    return {
      sharelinkColour: null
    }
  }
})

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

// get rid of the annoying production tip
Vue.config.productionTip = false;

// main Vue instance
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
});
