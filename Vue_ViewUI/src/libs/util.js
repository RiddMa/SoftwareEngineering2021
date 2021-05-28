/**
 * 工具类
 * @type {{validateTemp: (function(*)), fixFocus: util.fixFocus, title: util.title, validateWind: (function(*))}}
 */
let util = {
    /**
     * 设置网页标题
     * @param title
     */
    title: function (title) {
        title = title ? title + '' : '加载中';
        window.document.title = title;
    },
    /***
     * 验证温度是否合法
     * @param targetTemp 目标温度
     * @returns {boolean} 是否合法
     */
    validateTemp: function (targetTemp) {
        let low = 16, high = 30;
        return (low <= targetTemp && targetTemp <= high);
    },
    /**
     * 验证风速是否合法
     * @param targetWind 目标风速
     * @returns {boolean} 是否合法
     */
    validateWind: function (targetWind) {
        let low = 1, high = 3;
        return (low <= targetWind && targetWind <= high);
    },
    /**
     * 修正焦点，暂时无用
     * @param e
     */
    fixFocus: function (e) {
        let target = e.target;
        if (target.nodeName === "SPAN") {
            target = e.target.parentNode;
        }
        target.blur();
    }
};


export default util;
