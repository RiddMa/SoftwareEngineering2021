const routers = [
    {
        path: '/client',
        meta: {
            title: 'client'
        },
        component: (resolve) => require(['./views/client.vue'], resolve)
    },
    {
        path:'/admin',
        meta:{
            title:'admin'
        },
        component: (resolve) => require(['./views/admin.vue'], resolve)
    },
    {
        path:'/',
        meta:{
            title:'welcome'
        },
        component: (resolve) => require(['./views/welcome.vue'], resolve)
    },

];
export default routers;