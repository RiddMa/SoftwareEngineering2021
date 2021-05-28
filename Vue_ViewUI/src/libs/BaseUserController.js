/**
 * 用户控制器，登录登出
 * @type {{}}
 */
let BaseUserController = {
    userLogin: function (userType, username, password) {
        switch (userType) {
            case 'client':
                this.$router.push({path: '/client'});
                break;
            case 'admin':
                this.$router.push({path: '/admin/main'});
                break;
            case 'reception':
                this.$router.push({path: '/reception/main'});
                break;
            case 'manager':
                this.$router.push({path: '/manager/daily'});
                break;
            default:
                alert('userType error!');
        }
    },
}
export default BaseUserController;