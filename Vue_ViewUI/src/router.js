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
        path: '/admin/login',
        meta: {
            title: '管理员登录',
        },
        component: (resolve) => require(['./views/adminView/adminLogin'], resolve),
    },
    {
        path: '/admin',
        // keepalive:true,
        meta: {
            title: '管理员'
        },
        component: (resolve) => require(['./views/adminView/admin.vue'], resolve),
        children: [
            {
                path: 'main',
                meta: {
                    title: '管理员概览'
                },
                component: (resolve) => require(['./views/adminView/adminMain.vue'], resolve),
            },
            {
                path: 'search',
                meta: {
                    title: '管理员搜索'
                },
                component: (resolve) => require(['./views/adminView/adminSearch.vue'], resolve),
            },
            {
                path: 'settings',
                meta: {
                    title: '管理员设置'
                },
                component: (resolve) => require(['./views/adminView/adminSettings.vue'], resolve),
            },

        ]
    },

    {
        path: '/reception',
        meta: {
            title: '前台',
        },
        component: (resolve) => require(['./views/receptionView/reception'], resolve),
        children: [
            {
                path: 'main',
                meta: {
                    title: '前台登记'
                },
                component: (resolve) => require(['./views/receptionView/receptionMain.vue'], resolve),
            },
            {
                path: 'search',
                meta: {
                    title: '前台搜索'
                },
                component: (resolve) => require(['./views/receptionView/receptionSearch.vue'], resolve),
            },
            {
                path: 'settings',
                meta: {
                    title: '前台设置'
                },
                component: (resolve) => require(['./views/receptionView/receptionSettings.vue'], resolve),
            },
        ]
    },

    {
        path: '/reception/login',
        meta: {
            title: '前台登录',
        },
        component: (resolve) => require(['./views/receptionView/receptionLogin'], resolve),

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