let util = {

};
util.title = function (title) {
    title = title ? title + '' : '加载中';
    window.document.title = title;
};

export default util;
