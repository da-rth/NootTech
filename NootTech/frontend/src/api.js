import axios from 'axios'
import store from './store'
import router from './router'

axios.defaults.xsrfHeaderName = "X-CSRFToken"

/**
 * Configures AXIOS to send JWT token in header of each API request for user.is_authenticated API calls
 */
if (store.state.token) {
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
}

/**
 * @returns {string} - The base API url. Remove :8000 before deployment!
 */
export function base () {
  return 'http://' + window.location.hostname + ':8000/api'
}

export async function GetErrorVideos () {
  console.log("Attempting to get list of error videoss...");
  return axios.get(base() + '/error-videos/')
    .then(response => {
      console.log('ERROR VIDEO SUCCESS', response)
      console.log(response)
      return response.data
    })
    .catch(e => {
      console.log(e)
      return null
    })
}

export async function GetSettings () {
  console.log("Attempting to get user settings...");
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
  console.log("Attempting to get user files...");
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


export async function DeleteFile (file_id) {
  console.log("Attempting to delete file with ID: "+file_id);
  const res = axios.delete(base()+'/file/delete/'+file_id)
    .then(response => {
      console.log('DELETE SUCCESS', response);
      return response.data
    })
    .catch(e => {
      console.log('ERROR', e.response);
      return null
    });
  return await res
}


export async function GetShareData (username, gen_name) {
    const res = axios.get(base()+`/sharelink/${username}/${gen_name}`)
        .then(response => {
            console.log('SHARELINK SUCCESS!',  response.data);
            return response.data;
        })
        .catch(e => {
            console.log('SHARELINK ERROR...');
        });
    return await res
}
