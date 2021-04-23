let util = {

};
util.title = function (title) {
    title = title ? title + ' - 主页' : '加载中';
    window.document.title = title;
};

export default util;
