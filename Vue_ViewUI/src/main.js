import 'es6-promise/auto';
import Vue from 'vue';
import Vuex from 'vuex';
import ViewUI from 'view-design';
import VueRouter from 'vue-router';
import axios from 'axios'
import VueAxios from 'vue-axios'
import Routers from './router';
import Util from './libs/util';
import App from './app.vue';
import admin from './views/adminView/admin.vue';
import clientLogin from "./views/clientView/clientLogin";
import client from "./views/clientView/client";
import adminMain from "./views/adminView/adminMain";
import adminSearch from "./views/adminView/adminSearch";
import adminLogin from "./views/adminView/adminLogin";
import adminSettings from "./views/adminView/adminSettings";
import 'view-design/dist/styles/iview.css';

Vue.use(Vuex);
Vue.use(VueRouter);
Vue.use(ViewUI);
Vue.use(VueAxios, axios);


// 路由配置
const RouterConfig = {
    mode: 'history',
    routes: Routers
};
const router = new VueRouter(RouterConfig);

// 进度条配置
router.beforeEach((to, from, next) => {
    ViewUI.LoadingBar.start();
    Util.title(to.meta.title);
    next();
});
router.afterEach((to, from, next) => {
    ViewUI.LoadingBar.finish();
    window.scrollTo(0, 0);
});

// Vuex仓库配置
const store = new Vuex.Store({
    state: {
        CACState: false,//CAC for Central Air-Conditioning
        sessionData: Object.create(null),
        roomInfo: Object.create(null),
        // roomInfo: Map.create(null)
    },
    mutations: {}
})


new Vue({
    el: '#app',
    router: router,
    store: store,
    render: h => h(App)
});
