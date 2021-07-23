import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import App from "./App.vue";
import "./index.css";

import HomePage from "./components/HomePage/HomePage.vue";
import SparcLink from "./components/SparcLink/SparcLink.vue";
import SparclinkSvg from "./components/SparcLink/SparclinkSvg.vue";

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior: function (to) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: "smooth",
      };
    } else {
      window.scrollTo(0, 0);
    }
  },
  routes: [
    { path: "/", name: "root", redirect: "/home" },
    { path: "/home", component: HomePage },
    { path: "/sparclink", component: SparcLink },
    { path: "/SparclinkSvg", component: SparclinkSvg },
  ],
});

const app = createApp(App);

app.use(router);

app.mount("#app");
