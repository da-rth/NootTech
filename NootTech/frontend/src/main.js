import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import * as backendAPI from './api.js'
import config from './config.json';
import VuePaginate from 'vue-paginate'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import VueVideoPlayer from 'vue-video-player'
import Notifications from 'vue-notification'
import VueHighlightJS from 'vue-highlight.js'

// CSS Imports
import 'video.js/dist/video-js.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'highlight.js/styles/monokai-sublime.css';
import './assets/css/main.css'

// HighlightJS Imports
import python from 'highlight.js/lib/languages/python'
import diff from 'highlight.js/lib/languages/diff'
import html from 'highlight.js/lib/languages/xml'
import erlang from 'highlight.js/lib/languages/erlang'
import java from 'highlight.js/lib/languages/java'
import coffee from 'highlight.js/lib/languages/coffeescript'
import javascript from 'highlight.js/lib/languages/javascript'
import json from 'highlight.js/lib/languages/json'
import perl from 'highlight.js/lib/languages/perl'
import xml from 'highlight.js/lib/languages/xml'
import lua from 'highlight.js/lib/languages/lua'
import ruby from 'highlight.js/lib/languages/ruby'
import haskell from 'highlight.js/lib/languages/haskell'
import php from 'highlight.js/lib/languages/php'
import bash from 'highlight.js/lib/languages/bash'
import smalltalk from 'highlight.js/lib/languages/smalltalk'
import rust from 'highlight.js/lib/languages/rust'
import r from 'highlight.js/lib/languages/r'
import css from 'highlight.js/lib/languages/css'
import applescript from 'highlight.js/lib/languages/applescript'
import apache from 'highlight.js/lib/languages/apache'
import brainfuck from 'highlight.js/lib/languages/brainfuck'
import cmake from 'highlight.js/lib/languages/cmake'
import clojure from 'highlight.js/lib/languages/clojure'
import c from 'highlight.js/lib/languages/cpp'
import cpp from 'highlight.js/lib/languages/cpp'
import dos from 'highlight.js/lib/languages/dos'
import django from 'highlight.js/lib/languages/django'
import fsharp from 'highlight.js/lib/languages/fsharp'
import cs from 'highlight.js/lib/languages/cs'
import http from 'highlight.js/lib/languages/http'
import ini from 'highlight.js/lib/languages/ini'
import markdown from 'highlight.js/lib/languages/markdown'
import nginx from 'highlight.js/lib/languages/nginx'
import d from 'highlight.js/lib/languages/d'
import objectivec from 'highlight.js/lib/languages/objectivec'
import scilab from 'highlight.js/lib/languages/scilab'
import vbnet from 'highlight.js/lib/languages/vbnet'
import vbscript from 'highlight.js/lib/languages/vbscript'
import GitHubAPI from 'vue-github-api'
import VueResource from 'vue-resource'

Vue.use(VueResource)
Vue.use(GitHubAPI, { token: config.GITHUB_TOKEN })
Vue.use(VueHighlightJS, {
  languages: {
    python, html, erlang, java, coffee, javascript, json, perl, xml, lua, ruby, diff,
    haskell, php, bash, smalltalk, rust, r, css, applescript, apache, brainfuck, cmake,
    clojure, c, cpp, dos, django, fsharp, cs, http, ini, markdown, nginx, d, objectivec,
    scilab, vbnet, vbscript
  }
});



// register FontAwesome fonts
library.add(fas);
library.add(far);
library.add(fab);

Vue.component('font-awesome-icon', FontAwesomeIcon);

// Enable a bunch of Vue plugins
Vue.use(VuePaginate);
Vue.use(VueVideoPlayer);
Vue.use(Notifications);
//Vue.use(BootstrapVue);

import { Alert, Button, ButtonGroup, Card, Carousel, Collapse,
         Dropdown, Form, FormFile, FormGroup, FormInput, FormSelect,
         FormTextarea, InputGroup, Jumbotron, Layout, Modal, Nav, Navbar,
         Tabs}
         from 'bootstrap-vue/es/components';

Vue.use(Alert);
Vue.use(Button);
Vue.use(ButtonGroup);
Vue.use(Card);
Vue.use(Carousel);
Vue.use(Collapse);
Vue.use(Dropdown);
Vue.use(Form);
Vue.use(FormFile);
Vue.use(FormGroup);
Vue.use(FormInput);
Vue.use(FormSelect);
Vue.use(FormTextarea);
Vue.use(InputGroup);
Vue.use(Jumbotron);
Vue.use(Layout);
Vue.use(Modal);
Vue.use(Nav);
Vue.use(Navbar);
Vue.use(Tabs);

Vue.prototype.$api = backendAPI;
Vue.prototype.$site_url = config.SITE_URL;
Vue.prototype.$backend_url = config.BACKEND_URL;
Vue.prototype.$subdomain_enabled = config.ENABLE_SUBDOMAINS;

Vue.mixin({
  data: function () {
    return {
      colour: config.DEFAULT_HIGHLIGHT,
      default_colour: config.DEFAULT_HIGHLIGHT,
      sharelinkName: null,
      popupFileModalFile: null,
      files: [],
      selected_files: [],
      searched_files: [],
      favourite_files: [],
    }
  },
  methods: {
    toggleFile (fileId) {
      if(this.selected_files.includes(fileId))
        this.selected_files.splice(this.selected_files.indexOf(fileId), 1);
      else this.selected_files.push(fileId);
    },
  }
})

// get rid of the annoying production tip
Vue.config.productionTip = false;

// main Vue instance
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
});
