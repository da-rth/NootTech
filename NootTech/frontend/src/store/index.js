import Vuex from 'vuex'
import Vue from 'vue'
import * as types from './mutation-types'
import axios from 'axios'
import createPersistedState from 'vuex-persistedstate'
import router from '../router'
import * as config from '../config.js';

import * as authentication from '../api.js';

Vue.use(Vuex);

const state = {
  user: null,
  token: null,
  settings: null,
};

const mutations = {
  [types.LOGIN]: (state, payload) => {
    state.token = payload.token;
    state.user = payload.user;
    router.push(payload.redirect);
  },
  [types.SETTINGS]: (state, settings) => {
    state.settings = settings;
  },
  [types.LOGOUT]: (state, payload) => {
    state.token = null;
    state.user = null;
    state.settings = null;
    router.push(payload.redirect);
  },
  [types.REFRESH]: (state, data) => {
    state.token = data.token;
  },
  [types.REGISTER]: (state, payload) => {
    router.push(payload.redirect);
  }
};

const actions = {

  /**
   * Try to log in, store the user token and the settings
   * @param {Object} payload
   * @param {Object} payload.credentials - username+password
   * @param {string} payload.redirect - the url to redirect to if the authentication succeeds
   */
  async [types.LOGIN] ({ commit, dispatch }, payload) {
    const mutationPayload = await authentication.login(payload.credentials);
    mutationPayload.redirect = payload.redirect;
    console.log("Authentication successfully performed");
    dispatch(types.SETTINGS);
    commit(types.LOGIN, mutationPayload);
  },
  async [types.SETTINGS] ({ commit }) {
    commit(types.SETTINGS, await authentication.GetSettings());
  },
  async [types.REGISTER] ({ commit, dispatch }, payload) {
    try {
      await authentication.register(payload.credentials);
      console.log("Account created!");
      commit(types.REGISTER, payload.redirect);
    } catch(error) {
      console.log("Can't register a new user: ", error);
    }
  },
  async [types.VERIFY] ({ commit }, payload) {
    try {
      let response = await authentication.verifyToken(payload.token);
      if(response.data.token) {
        console.log('The token has been verified');
      } 
    } catch(error) {
      console.log("Can't authenticate the token, cause: ", error);
      console.log('Un-authenticated token, logging out.');
      commit(types.LOGOUT, {redirect: payload.redirect});
    }
  },
  async [types.REFRESH] ({ commit }, payload) {
    try {
      commit(types.REFRESH, {token: await authentication.refreshToken(payload.token)});
    } catch(error) {
      console.log("Couldn't refresh the token: ", error);
    }
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

export default store;
