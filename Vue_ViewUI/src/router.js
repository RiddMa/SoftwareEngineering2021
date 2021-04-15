const routers = [
    {
        path: '/client/login',
        meta: {
            title: '客户端登录'
        },
        component: (resolve) => require(['./views/clientView/clientLogin.vue'], resolve),
        children: []
    },


    {
        path: '/client',
        meta: {
            title: '客户端'
        },
        component: (resolve) => require(['./views/clientView/client.vue'], resolve),
    },


    {
        path: '/admin',
        meta: {
            title: 'admin'
        },
        component: (resolve) => require(['./views/adminView/admin.vue'], resolve)
    },
    {
        path: '/',
        meta: {
            title: 'welcome'
        },
        component: (resolve) => require(['./views/welcome.vue'], resolve)
    },
    {
        path: '/netInterfaceTest',
        meta: {
            title: '全按钮测试'
        },
        component: (resolve) => require(['./views/netInterfaceTest'], resolve)
    },


];
export default routers;