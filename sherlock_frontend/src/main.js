import axios from "axios";
import { createApp } from "vue";
import VueMarkdownIt from "vue3-markdown-it";

import App from "./App.vue";
import router from "./router";
import store from "./store";

import "./../node_modules/bulma/css/bulma.css";
import "./../node_modules/chartist/dist/chartist.min.css";
import "./assets/css/chartist_custom.css";
import "./assets/css/sherlock_custom.css";

// Full config:  https://github.com/axios/axios#request-config
axios.defaults.baseURL = "http://127.0.0.1:5000/api";

var tokenData = JSON.parse(window.localStorage.getItem("authentication_data"));

if (tokenData) {
  axios.defaults.headers.common["Authorization"] = "Bearer " + tokenData.token;
  axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
} else {
  console.log("token errado");
}

createApp(App)
  .use(store)
  .use(router)
  .use(VueMarkdownIt)
  .mount("#app");
