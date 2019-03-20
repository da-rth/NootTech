import Vue from 'vue'
import Router from 'vue-router'
//import store from '../store'

//import Subdomain from '@/components/Subdomain'
import AdminPanel from '../components/Authentication/AdminPanel'
import Base from '../components/Index'
import SharePage from '../components/Navigation/SharePage'
import About from '../components/About'
import TermsOfService from '../components/ToS'
import LoginRegister from '../components/Authentication/LoginRegister'
import Logout from '../components/Authentication/Logout'
import PageNotFound from '../components/Navigation/PageNotFound'
import Privacy from '../components/Privacy'
import HowTo from '../components/HowTo'

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
    component: LoginRegister
  },
  {
    path: '/logout',
    name: 'Logout',
    component: Logout
  },
  {
    path: '/moderate',
    name: 'AdminPanel',
    component: AdminPanel
  },
  {
    path: '/how-to',
    name: 'HowTo',
    component: HowTo
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/privacy',
    name: 'PrivacyPolicy',
    component: Privacy
  },
  {
    path: '/terms',
    name: 'TermsOfService',
    component: TermsOfService
  },
  {
    path: '/u/:username/:gen_name',
    name: 'ShareLink',
    component: SharePage
  },
  {
    path: '/404',
    name: '404',
    component: PageNotFound
  },
  {
    path: '*',
    redirect: '/404'
  }
]

const router = new Router({
  routes,
  mode: 'history'
});


router.beforeEach((to, from, next) => {
  if (to.meta.requireAuth) {
    if (store.state.token != null) {
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
})

export default router
