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
import 'view-design/dist/styles/iview.css';

var test = '123';

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
        roomInfo:Object.create(null)
    },
    mutations: {
        /**
         *
         * @param state Vuex的仓库状态对象，原样传入即可
         * @param newData 一个包含key和value键的键值对，const testData = {key: 'uid123', value: '456username'};
         * 传入之后在sessionData里存储结构是 uid123:'456username'
         */
        addSessionData(state, newData) {
            Vue.set(state.sessionData,newData.key,newData.value)
        },
        delSessionData(state, delData) {
            Vue.delete(state.sessionData,delData.key)
        },
        /**
         * 以上方法可以存入任意键值对
         * 如果不行则采用下面方法向Vuex已经声明好的变量写入值
         */
        // setRoomId(state, roomId) {
        //     state.roomId = roomId;
        // },
        // setTokenAdmin(state, tokenAdmin) {
        //     state.tokenAdmin = tokenAdmin;
        // },
        // setTokenUser(state, tokenUser) {
        //     state.tokenUser = tokenUser;
        // }
    }
})


new Vue({
    el: '#app',
    router: router,
    store: store,
    render: h => h(App)
});
