import axios from 'axios'
import store from './store'
import router from './router'

axios.defaults.xsrfHeaderName = "X-CSRFToken"

/**
 * Configures AXIOS to send JWT token in header of each API request for user.is_authenticated API calls
 */
axios.interceptors.request.use(
  config => {
    if (store.state.token) {
      config.headers.Authorization = `JWT ${store.state.token}`
    }
    return config
  },
  err => {
    return Promise.reject(err)
  })

/**
 * If unable to get valid response with JWT token, log user out (deletes token)
 */
axios.interceptors.response.use(
  response => {
    return response
  },
  error => {
    console.log('[Response error!]', error.response)
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // Using logout instead of login for renew state
          store.commit('LOGOUT', {
            router: router,
            redirect: router.currentRoute.fullPath
          });
          break;
        case 500:
          console.log(error.response.statusText)
          break
      }
    }
    return Promise.reject(error.response.data)
  });

/**
 * @returns {string} - The base API url. Remove :8000 before deployment!
 */
export function base () {
  return 'http://' + window.location.hostname + ':8000/api'
}

export async function GetErrorVideos () {
  return axios.get(base() + '/error-videos/')
    .then(response => {
      console.log(response)
      return response.data
    })
    .catch(e => {
      console.log(e)
      return null
    })
}

export async function GetSettings () {
  const res = axios.get(base() + '/settings/')
    .then(response => {
      console.log('SETTINGS SUCCESS', response)
      return response.data[0]
    })
    .catch(e => {
      console.log('ERROR', e.response);
      return null
    });
  return await res
}

export async function GetFiles () {
  const res = axios.get(base()+'/files/')
    .then(response => {
      console.log('FILES SUCCESS', response);
      return response.data
    })
    .catch(e => {
      console.log('ERROR', e.response);
      return null
    });
  return await res
}

/*
Will implement later...

export async function GetFile (url) {
    const res = axios.get(url)
        .then(response => {
            console.log('Success!');
            return response.data;
        })
        .catch(e => {
            console.log(e);
            return 'Could not get file contents';
        });
    return await res
}

export async function SubdomainRequest (username, gen_name) {
    const res = axios.get(base()+`/get/subdomain?username=${username}&gen_name=${gen_name}`)
        .then(response => {
            console.log('Success!');
            return response.data;
        })
        .catch(e => {
            console.log(e);
            return 'Could not establish subdomain... should redirect';
        });
    return await res
}
*/
