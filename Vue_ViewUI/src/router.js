const routers = [
    {
        path: '/client/login',
        meta: {
            title: '客户端登录'
        },
        component: (resolve) => require(['./views/ClientView/ClientLogin.vue'], resolve),
        children: []
    },
    {
        path: '/client',
        meta: {
            title: '客户端'
        },
        component: (resolve) => require(['./views/ClientView/Client.vue'], resolve),
    },

    {
        path: '/admin/login',
        meta: {
            title: '管理员登录',
        },
        component: (resolve) => require(['./views/AdminView/AdminLogin'], resolve),
    },
    {
        path: '/admin',
        // keepalive:true,
        meta: {
            title: '管理员'
        },
        component: (resolve) => require(['./views/AdminView/Admin.vue'], resolve),
        children: [
            {
                path: 'main',
                meta: {
                    title: '管理员概览'
                },
                component: (resolve) => require(['./views/AdminView/AdminMain.vue'], resolve),
            },
            {
                path: 'search',
                meta: {
                    title: '管理员搜索'
                },
                component: (resolve) => require(['./views/AdminView/AdminSearch.vue'], resolve),
            },
            {
                path: 'settings',
                meta: {
                    title: '管理员设置'
                },
                component: (resolve) => require(['./views/AdminView/AdminSettings.vue'], resolve),
            },

        ]
    },

    {
        path: '/reception/login',
        meta: {
            title: '前台登录',
        },
        component: (resolve) => require(['./views/ReceptionView/ReceptionLogin'], resolve),

    },
    {
        path: '/reception',
        meta: {
            title: '前台',
        },
        component: (resolve) => require(['./views/ReceptionView/Reception'], resolve),
        children: [
            {
                path: 'main',
                meta: {
                    title: '前台登记'
                },
                component: (resolve) => require(['./views/ReceptionView/ReceptionMain.vue'], resolve),
            },
            {
                path: 'search',
                meta: {
                    title: '前台搜索'
                },
                component: (resolve) => require(['./views/ReceptionView/ReceptionSearch.vue'], resolve),
            },
            {
                path: 'settings',
                meta: {
                    title: '前台设置'
                },
                component: (resolve) => require(['./views/ReceptionView/ReceptionSettings.vue'], resolve),
            },
        ]
    },

    {
        path: '/manager/login',
        meta: {
            title: '经理登录',
        },
        component: (resolve) => require(['./views/ManagerView/ManagerLogin.vue'], resolve),

    },
    {
        path: '/manager',
        meta: {
            title: '经理',
        },
        component: (resolve) => require(['./views/ManagerView/Manager'], resolve),
        children: [
            {
                path: 'daily',
                meta: {
                    title: '日报'
                },
                component: (resolve) => require(['./views/ManagerView/ManagerDaily.vue'], resolve),
            },
            {
                path: 'weekly',
                meta: {
                    title: '周报'
                },
                component: (resolve) => require(['./views/ManagerView/ManagerWeekly.vue'], resolve),
            },
            {
                path: 'settings',
                meta: {
                    title: '前台设置'
                },
                component: (resolve) => require(['./views/ManagerView/ManagerSettings.vue'], resolve),
            },
        ]
    },
    
    {
        path: '/',
        meta: {
            title: 'welcome'
        },
        component: (resolve) => require(['./views/Welcome.vue'], resolve)
    },

    {
        path: '/netInterfaceTest',
        meta: {
            title: '全按钮测试'
        },
        component: (resolve) => require(['./views/NetInterfaceTest'], resolve)
    },
];
export default routers;