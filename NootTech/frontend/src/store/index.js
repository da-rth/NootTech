import Vuex from 'vuex'
import Vue from 'vue'
import * as types from './mutation-types'
import axios from 'axios'
import createPersistedState from 'vuex-persistedstate'
import router from '../router'


const API_URL = 'http://' + window.location.hostname + ':8000/api';
const LOGIN_URL = API_URL + '/token/auth/';
const REGISTER_URL = API_URL + '/create-user/';
const REFRESH_URL = API_URL + '/token/refresh/';
const VERIFY_URL = API_URL + '/token/verify/';

Vue.use(Vuex);

const state = {
  user: {},
  token: null
};

const mutations = {
  [types.LOGIN]: (state, payload) => {
    state.token = payload.token;
    state.user = payload.user;
    router.push(payload.redirect)
  },
  [types.LOGOUT]: (state, payload) => {
    state.token = null;
    state.user = {};
    router.push(payload.redirect)
  },
  [types.REFRESH]: (state, data) => {
    state.token = data.token
  },
    [types.REGISTER]: (state, payload) => {
    router.push(payload.redirect)
  }
};

const actions = {

  [types.LOGIN] ({ commit }, payload) {
      return new Promise((resolve, reject) => {
          axios.post(LOGIN_URL, payload.credentials)
              .then( (response) => {
                console.log("Logging user in...")
                  if (response.data.token) {
                      const mutationPayload = {};
                      mutationPayload.token = response.data.token;
                      mutationPayload.user = JSON.parse(atob(response.data.token.split('.')[1]));
                      mutationPayload.user.authenticated = true;
                      mutationPayload.redirect = payload.redirect;
                      commit(types.LOGIN, mutationPayload);
                      resolve();
                  }
              }, (error) => reject(error))
      });
  },

    [types.REGISTER] ({ commit, dispatch }, payload) {
        return new Promise((resolve, reject) => {
            axios.post(REGISTER_URL, payload.credentials)
                .then( (response) => {
                      console.log('Account created!')
                      dispatch(types.LOGIN, payload)
                      commit(types.REGISTER, payload.redirect);
                      resolve();
                }, (error) => reject(error))
        });
    },

  [types.VERIFY] ({ commit }, payload) {
    let mutationPayload = {redirect: payload.redirect};
    axios.post(VERIFY_URL, {token: payload.token})
      .then(response => {
        if (response.data.token) {
          console.log('Token verified.')
        }
      })
      .catch(e => {
        console.log('Un-authenticated token, logging out.');
        commit(types.LOGOUT, mutationPayload)
      })
  },

  [types.REFRESH] ({ commit }, payload) {
    axios.post(REFRESH_URL, payload)
      .then(response => {
        if (response.data.token) {
          var mutationPayload = {token: response.data.token};
          commit(types.REFRESH, mutationPayload)
        }
      })
      .catch(e => {
        console.log('REFRESH TOKEN ERROR', e.response)
      })
  },

};

const store = new Vuex.Store({
  state,
  mutations,
  actions,
  plugins: [
    createPersistedState()
  ]
});

export default store
