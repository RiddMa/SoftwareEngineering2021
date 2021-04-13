# 软件工程

## 前端

* 目录：Vue_ViewUI
* 使用方法：

```terminal
npm install
npm run init
npm run dev
```
### 目录树
* src：源文件
    * styles：
        * common.css：没啥用的全局样式
    * views：vue视图组件
      * adminView
        * admin.vue：管理员端
      * clientView：
        * client.vue：客户端
        * clientLogin.vue：客户端登录
      * receptionView：
        * reception.vue：前台端
      * connect.vue：网络连接组件
      * welcome.vue：选择登录某端（开发用）
    * app.vue：根组件
    * main.js：主入口
    * router.js：路由配置
    
* babelrc等：配置文件

## 后端

* 目录：flask_project
* 使用方法：

需要提前装好python工具包

```
python -m pip install flask
python -m pip install flask_cors
python -m pip install sqlalchemy
python -m pip install flask_sqlalchemy
python app.py
```
### 目录树
* app.py：主函数入口，通信模块
* db.py：数据库操作模块
* model.py：服务器处理模块
* \_\_pycache\_\_：编译字节码
* templates：某些零碎的东西



