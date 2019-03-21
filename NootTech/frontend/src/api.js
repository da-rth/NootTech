import axios from 'axios'
import config from './config.json';



const API_URL = config.API_URL
// Authentication & Settings
const LOGIN_URL = API_URL + '/token/auth/';
const REFRESH_URL = API_URL + '/token/refresh/';
const REGISTER_URL = API_URL + '/create-user/';
const VERIFY_URL = API_URL + '/token/verify/';

// File Management
const FILE_URL = API_URL + '/file/';
const FILES_URL = API_URL + '/files/';

// User Upload & Settings
const SETTINGS_URL = API_URL + '/settings/';
const CHANGE_PASSWORD_URL = API_URL + '/change-password/';
const DELETE_ACCOUNT_URL = API_URL + '/delete-account';
const UPLOAD_URL = API_URL + '/upload/';

// Unauthenticated APIs
const SHARELINK_URL = API_URL + '/sharelink/';
const ERROR_VIDEOS_URL = API_URL + '/error-videos';

// Reporting
const REPORTS_URL = API_URL + '/reports';
const REPORT_FILE_URL = API_URL + '/report-file'

// Moderation
const WARNINGS_URL = API_URL + '/warnings';
const WARN_USER_URL = API_URL + '/warn';
const BAN_USER_URL = API_URL + '/ban';

// Favouriting
const FAVS_URL = API_URL + '/favourites'
const FAV_ADD_URL = API_URL + '/favourite/add'
const FAV_DEL_URL = API_URL + '/favourite/delete'

// Provide CSRF Token for authenticated requests
axios.defaults.xsrfHeaderName = "X-CSRFToken";

// A second instance of axios to be used for unauthenticated requests, such as previewing a sharelink or viewing an error video.
var axios_unauth = axios.create({ baseURL: config.API_URL });


// Globally Accessable AXIOS Functions


/**
 * Configures AXIOS to send JWT token in header of each API request for
 * user.is_authenticated API calls.
 * This function is invoked every time the user loges in.
 *
 * @param {string} token - the JWT token
 */

var auth_interceptor = null;

function setToken(token) {
  auth_interceptor = axios.interceptors.request.use(
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
  let response = await axios.post(LOGIN_URL, credentials);
  const parsedResponse = {}; parsedResponse.token = response.data.token;
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

/**
 * Configuses AXIOS to "forget" the authentication token.
 * Useful for logging out.
 */

export function flushToken() {
  axios.interceptors.request.eject(auth_interceptor);
  console.log("The token has been forgotten");
}

/**
 * Gets a list (array) of error videos, no authentication required.
 * Returns the data if promise is successful.
 */
export async function GetErrorVideos () {
  console.log("Attempting to get list of error videos...");
  return axios.get(ERROR_VIDEOS_URL)
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
 * @returns {Promise} A list of settings (object)
 */
export async function GetSettings () {
  let response = await axios.get(SETTINGS_URL);
  return response.data[0];
}

/**
 * Gets an array of file information of all files uploaded by the currently authenticated user.
 */
export async function GetFiles () {
  return await axios.get(FILES_URL);
}
/**
 * Given a fileID, this will delete a file with such an ID if it belongs to the current user.
 * @param {int} fileID
 */
export async function DeleteFile (file_id) {
  return await axios.put(FILE_URL+file_id, {delete: true});
}

/**
 * Gets the file informaton needed to display a file preview whenever a user visit's another user's sharelink
 * @param {string} username the username belonging to the sharelink (http://{USERNAME}.noot.tech or http://noot.tech/u/{USERNAME}/{GEN_NAME}
 * @param {string} gen_name the generated filename belonging to a file uploaded by the above username
 */
export async function GetShareData (username, gen_name) {
  return await axios_unauth.get(SHARELINK_URL+`${username}/${gen_name}`)
}

/**
 * Upload an URL
 * @param {Object} payload the payload to load
 * @param {String} payload.upload_key the upload token required for uploading
 * @param {Boolean} payload.is_private the private uploading flag
 * @param {Blob[]} payload.files an array of blob resources to load
 * @param {string} payload.username the uploader's username
 */
export async function UploadFiles(payload) {
  console.log("Attempting to upload a file", payload);
  let formData = new FormData();
  //formData.set('private', Boolean(is_private))
  formData.set('upload_key', payload.upload_key);
  formData.set('username', payload.username);
  formData.set('is_private', payload.is_private);

  payload.files.forEach((file => {
    formData.append(`content`, file, file.name);
  }));

  return await axios.post(UPLOAD_URL, formData, { headers: { 'Content-Type': 'multipart/form-data' } });
}

/**
 * @param {string} url - Gets the content of a file given it's URL. This is used to display the contents of text-files for highlightjs
 */
export async function GetFile(url) {
  // Gets the content of a specified URL (used for highlightjs)
  return await axios_unauth.get(url);
}

/**
 * Set modify the settings of currently authenticated user
 * @param {Object} settings the user's settings to be updated (email, password, gen_key, colour)
 */
export async function UpdateSettings(settings) {
  return await axios.post(SETTINGS_URL, settings);
}

/**
 * Toggle the privacy of a file belonging to currently authenticated user
 * @param {int} fileID the ID of the file to be toggled
 */
export async function TogglePrivacy(fileID) {
  return await axios.put(`${FILE_URL}${fileID}`, {toggle_private: true});
}

/**
 * Report a file given sufficient information
 * @param {Object} reportInfo
 *  * reported_file (int)
 *  * reason_title (str)
 *  * reason_body (str)
 */
export async function ReportFile(reportInfo) {
  return await axios_unauth.post(REPORT_FILE_URL, reportInfo);
}

/**
 * Report a file, given sufficient information is supplied.
 * @param {Object} reportInfo
 *  * reason (str, optional)
 *  * warned_user (int, User ID)
 */
export async function WarnUser(warnInfo) {
  return await axios.post(WARN_USER_URL, warnInfo);
}

/**
 * Ban a user, given the User ID is supplied.
 * @param {Object} banInfo
 *  * reason (str, optional)
 *  * banned_user (int, User ID)
 */
export async function BanUser(banInfo) {
  return await axios.post(BAN_USER_URL, banInfo);
}

/**
 * Get a list (array) of user-submitted reports (Administrator Only)
 */
export async function GetReports() {
  return await axios.get(REPORTS_URL);
}

/**
 * Get a list (array) of warnings for currently authenticated user
 */
export async function GetWarnings() {
  return await axios.get(WARNINGS_URL);
}

/**
 * Get a list of files that have been favourited by the currently authenticated user
 */
export async function GetFavourites() {
  return await axios.get(FAVS_URL);
}

/**
 * Given a file ID, add the file to the user's favourites list.
 * @param {int} fileID the file ID they refer to
 */
export async function AddFavourite(fileID) {
  return await axios.post(`${FAV_ADD_URL}/${fileID}`)
}

/**
 * Given a file ID, remove the file from the user's favourites list.
 * @param {int} fileID
 */
export async function DeleteFavourite(fileID) {
  return await axios.delete(`${FAV_DEL_URL}/${fileID}`)
}

/**
 * Change the user password
 * 
 * @param {String} oldPassword Old password (for confirmation purpuoses)
 * @param {String} newPassword New Password
 */
export async function ChangePassword(oldPassword, newPassword) {
  return await axios.post(CHANGE_PASSWORD_URL, {old_password: oldPassword,
                                                new_password: newPassword})

}

/**
 * Delete the user
 * 
 * Remember to invoke a logout function as this function does not flush the JWT token.
 * 
 * @param {String} confirmationPassword
 */
export async function DeleteAccount(confirmationPassword) {
  return await axios.post(DELETE_ACCOUNT_URL, {confirmation_password: confirmationPassword});
}

/**
 * Export the current state of axios. USE WITH CARE!
 */
export const _axios = axios;
