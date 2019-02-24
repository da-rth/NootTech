import axios from 'axios'
import * as config from './config.js';

const API_URL = config.API_URL
const FILE_URL = API_URL + '/file';
const FILES_URL = API_URL + '/files/';
const LOGIN_URL = API_URL + '/token/auth/';
const REFRESH_URL = API_URL + '/token/refresh/';
const REGISTER_URL = API_URL + '/create-user/';
const SETTINGS_URL = API_URL + '/settings/';
const SHARELINK_URL = API_URL + '/sharelink/';
const UPLOAD_URL = API_URL + '/upload/';
const VERIFY_URL = API_URL + '/token/verify/';

axios.defaults.xsrfHeaderName = "X-CSRFToken"

/**
 * Configures AXIOS to send JWT token in header of each API request for
 * user.is_authenticated API calls.
 * This function is invoked every time the user loges in.
 * TODO: choose whether to expose this function or not.
 *
 * @param {string} token - the JWT token
 */

function setToken(token) {
  axios.interceptors.request.use(
    config => {
      config.headers.Authorization = `JWT ${token}`;
      return config
    },
    err => {return Promise.reject(err);}
  )
}

/**
 * Authenticates the user and gets an authentication token.
 * Moreover, the new token will be automatically used for the next calls.
 * @param {Object} credentials
 * @param {string} credentials.username
 * @param {string} credentials.password
 * @returns {Promise} an Object `{user, token}`
 */
export async function login(credentials) {
  console.log("Attempting to log in...");
  let response = await axios.post(LOGIN_URL, credentials);
  const parsedResponse = {};
  parsedResponse.token = response.data.token;
  parsedResponse.user = JSON.parse(atob(response.data.token.split('.')[1]));
  // set the token for future API calls
  setToken(parsedResponse.token);
  return parsedResponse;
}

/**
 * Register a new user.
 *
 * N.B.: This call doesn't automatically log the user in, hence the `login()` function
 * should always be invoked.
 *
 * @param {Object} credentials
 * @param {string} credentials.username
 * @param {string} credentials.email
 * @param {string} credentials.password
 * @returns {Promise} an axios response encapsulated in a promise
 */
export async function register(credentials) {
  console.log("Attempting to register a user");
  return await axios.post(REGISTER_URL, credentials);
}

/**
 * checks if the current token is still valid.
 *
 * @param {string} token
 * @returns {Promise} an axios response encapsulated in a promise.
 * On success the response data should contain the same token
 */
export async function verifyToken(token) {
  setToken(token);
  return await axios.post(VERIFY_URL, {token});
}

/**
 * Check the current token and provide a new one.
 * The new token is automatically used
 *
 * @param {string} old_token - the old token
 * @returns {Promise} the new token (a `string`) encapsulated in a promise
 */

export async function refreshToken(old_token) {
  setToken(old_token);
  let response = await axios.post(REFRESH_URL, {old_token});
  new_token = response.data.token;
  setToken(new_token);
  return new_token;
}

export async function GetErrorVideos () {
  console.log("Attempting to get list of error videos...");
  return axios.get(API_URL + '/error-videos/')
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
/**
 * Get the user settings.
 * @returns {Promise} A list of settings
 */
export async function GetSettings () {
  console.log("Attempting to get user settings...");
  let response = await axios.get(SETTINGS_URL);
  return response.data[0];
}

export async function GetFiles () {
  console.log("Attempting to get user files...");
  return await axios.get(FILES_URL);
}

export async function DeleteFile (file_id) {
  console.log("Attempting to delete file with ID: "+file_id);
  return await axios.delete(FILE_URL+'delete/'+file_id)}


export async function GetShareData (username, gen_name) {
  return await axios.get(SHARELINK_URL+`${username}/${gen_name}`)
}

/**
 * Upload an URL
 * @param {Object} payload the payload to load
 * @param {String} payload.upload_key the upload token required for uploading
 * @param {Blob[]} payload.files an array of blob resources to load
 * @param {string} payload.username the uploader's username
 */
export async function UploadFiles(payload) {
  console.log("Attempting to upload a file", payload);
  let formData = new FormData();
  //formData.set('private', Boolean(is_private))
  formData.set('upload_key', payload.upload_key);
  formData.set('username', payload.username);
  payload.files.forEach((file => {
    formData.append(`content`, file, file.name);
  }));

  return await axios.post(UPLOAD_URL, formData, { headers: { 'Content-Type': 'multipart/form-data' } });
}
