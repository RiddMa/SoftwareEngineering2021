import Vue from 'vue';
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
import 'view-design/dist/styles/iview.css';

Vue.use(VueRouter);
Vue.use(ViewUI);
Vue.use(VueAxios, axios);

// 路由配置
const RouterConfig = {
    mode: 'history',
    routes: Routers
};
const router = new VueRouter(RouterConfig);

router.beforeEach((to, from, next) => {
    ViewUI.LoadingBar.start();
    Util.title(to.meta.title);
    next();
});

router.afterEach((to, from, next) => {
    ViewUI.LoadingBar.finish();
    window.scrollTo(0, 0);
});

new Vue({
    el: '#app',
    router: router,
    render: h => h(App)
});
