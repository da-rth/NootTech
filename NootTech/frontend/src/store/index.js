import Vuex from 'vuex'
import Vue from 'vue'
import * as types from './mutation-types.js'
import createPersistedState from 'vuex-persistedstate'
import router from '../router'
import * as authentication from '../api.js';

Vue.use(Vuex);

function default_state() {
  return {
    user: null,
    token: null,
    settings: null,
  }
}

const state = default_state();

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
    Object.assign(state, default_state());
    authentication.flushToken();
    router.push(payload.redirect);
  },
  [types.REFRESH]: (state, data) => {
    state.token = data.token;
  },
  [types.REGISTER]: (state, payload) => {
    router.push(payload.redirect);
  },
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
  /**
   * Update the user settings
   */
  async [types.SETTINGS] ({ commit }) {
    commit(types.SETTINGS, await authentication.GetSettings());
  },
  /**
   * Register a new user and logs in with the newly created account
   * @param {Object} payload
   * @param {Object} payload.credentials email+username+password
   * @param {Object} payload.redirect redirect url after registration succeeds
   */
  async [types.REGISTER] ({ commit, dispatch }, payload) {
    await authentication.register(payload.credentials);
    console.log("Account created!");
    dispatch(types.LOGIN, payload);
    // this step is not necessary as the route will be propagated anyway
    commit(types.REGISTER, payload.redirect);
},
  /**
   * Verify the current token. In case the token is invalid, apply for another
   * one
   * @param {Object} payload
   * @param {String} payload.token
   * @param {String} payload.redirect In case of failure, redirect to this page
   */
  async [types.VERIFY] ({ commit }, payload) {
    try {
      let response = await authentication.verifyToken(payload.token);
      if(response.data.token) {
        console.log('The token has been verified');
      }
    } catch(error) {
      console.log("Can't authenticate the token, cause: ", error.response.data);
      console.log('Un-authenticated token, logging out.');
      commit(types.LOGOUT, {redirect: payload.redirect});
    }
  },
  /**
   * Refresh the current token with a new token.
   * @param {Object} payload
   * @param {String} payload.token
   */
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