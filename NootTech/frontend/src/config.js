/**
 * SITE_URL is used by vue-route and serves as the basename of every
 * frontend route.
 * Remember to change me in a production environment!
 */
export const SITE_URL = "http://localhost:8080";
/**
 * BACKEND_URL is used by axios and vuex and serves as the basename of every
 * API call.
 * Remember to change me in a production environment!
 */
export const BACKEND_URL = "http://localhost:8000";
/**
 * Usually the API function calls should be under the BACKEND_URL,
 * feel free to modify this as you like.
 */
export const API_URL = BACKEND_URL+"/api";
/**
 * TODO: toggle ENABLE_SUBDOMAINS to enable subdomain usernames
 */
export const ENABLE_SUBDOMAINS = false;


export const DEFAULT_HIGHLIGHT = "#00cccc";
