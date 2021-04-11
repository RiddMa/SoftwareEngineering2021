const routers = [
    {
        path: '/',
        meta: {
            title: ''
        },
        component: (resolve) => require(['./views/client.vue'], resolve)
    }
];
export default routers;