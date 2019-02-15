import Vue from 'vue'
import Router from 'vue-router'
//import store from '../store'

//import Subdomain from '@/components/Subdomain'
import Base from '../components/Base'
import About from '../components/About'
import TermsOfService from '../components/ToS'
import Login from '../components/Authentication/Login'
import Logout from '../components/Authentication/Logout'
import Register from '../components/Authentication/Register'
import PageNotFound from '../components/Navigation/PageNotFound'


Vue.use(Router);

const routes = [
  {
    path: '/',
    name: 'Base',
    component: Base
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/logout',
    name: 'Logout',
    component: Logout
  },
    {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/tos',
    name: 'TermsOfService',
    component: TermsOfService
  },
  {
    path: "*", component: PageNotFound
  }
]
/*
  {
      path: '/subdomain/:username/:gen_name',
      name: 'Subdomain',
      component: Subdomain
  },

 */
const router = new Router({
  routes,
  mode: 'history'
});
/*
router.beforeEach((to, from, next) => {
  if (to.meta.requireAuth) {
    if (store.state.token) {
      next()
    } else {
      next({
        path: '/login',
        query: {redirect: to.fullPath}
      })
    }
  } else {
    next()
  }
})*/

export default router
