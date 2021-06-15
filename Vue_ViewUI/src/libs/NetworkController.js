import axios from "axios";
import Vue from "vue";
import store from "./store";

/**
 * 使用getInstance()方法获取唯一实例
 */
export class NetworkController {
	constructor() {
		this.serverURL = "http://192.168.43.159:5000/";
		// this.adminToken = this.dataStore.adminToken;
		// this.userToken = this.dataStore.userToken;
	}

	/**
	 * 惰性单例模式获取实例
	 * @returns {*}
	 */
	static getInstance() {
		if (!NetworkController.instance) {
			NetworkController.instance = new NetworkController();
		}
		return NetworkController.instance;
	}

	/**
	 * useless
	 * @param that
	 */
	testVue(that) {
		// Vue.set(that.$store.state.sessionData, 'test', 1);
		console.log(that.$store);
		that.$store.commit('setToken', {'userType': 0, 'token': '123'});
		console.log(that.$store);
	}

	/**
	 * 客户进入房间（登录）
	 * @param that
	 * @param roomId
	 * @param password
	 * @returns {Promise<number|*>} token
	 */
	async enterRoom(that, roomId, password) {
		try {
			let postURL = this.serverURL + "api/usr/signup";
			let response = await axios.post(postURL, {
				roomId: roomId,
				password: password
			});
			// Vue.set(that.$store.state.sessionData, 'tokenUser', response.data.data.token);
			that.$store.commit('setToken', {'userType': 0, 'token': response.data.token});
			return response.data.error_code;
		} catch (e) {
			console.log(e);
			return -1;//network error
		}
	}

	/**
	 * 通用登录方法，返回错误码
	 * @param that
	 * @param username 用户名
	 * @param password 密码
	 * @param userType 0-客户，1-管理员，2-前台，3-经理
	 * @returns {Promise<*>} 错误码0/1
	 */
	async login(that, username, password, userType) {
		// api/usr(mgr,ad,recp)/signup
		try {
			let postURL;
			switch (userType) {
				case 0:
					postURL = this.serverURL + "api/usr/signup";
					break;
				case 1:
					postURL = this.serverURL + "api/admin/signup";
					break;
				case 2:
					postURL = this.serverURL + "api/recp/signup";
					break;
				case 3:
					postURL = this.serverURL + "api/mgr/signup";
					break;
			}
			let response = await axios.post(postURL, {
				user: username,
				passwd: password
			});
			if (response.data.error_code === 0) {
				that.$store.commit('setToken', {'userType': userType, 'token': response.data.token});
			}
			return response.data.error_code;
		} catch (e) {
			console.log(e);
			return -1;//network error
		}

	}

	/**
	 * 用户请求开机
	 * @param that
	 * @param roomId 这tmd是个String！！！！！！
	 * @param toPower
	 * @returns {Promise<*>}
	 */
	async setUserPower(that, roomId, toPower) {
		if (toPower === true) {
			try {
				let newRoomState = that.$store.state.clientRoomState;
				let postURL = this.serverURL + "api/usr/poweron";
				let response = await axios.post(postURL, {
					roomId: roomId,
					targetTemp: newRoomState.targetTemp,
					fanSpeed: newRoomState.fanSpeed,
					currentTemp: newRoomState.currentTemp,
				});
				newRoomState.power = true;
				that.$store.commit('setClientRoomState', {'roomState': newRoomState});
				return response.data.error_code;
			} catch (e) {
				console.log(e);
				return -1;//network error
			}
		} else {
			try {
				let postURL = this.serverURL + "api/usr/poweroff";
				let response = await axios.post(postURL, {
					roomId: roomId
				});
				return response.data.error_code;
			} catch (e) {
				console.log(e);
				return -1;//network error
			}
		}
	}

	/**
	 * 发送心跳包
	 * @param that
	 * @param roomId
	 * @returns {Promise<number>}
	 */
	async heartBeat(that, roomId) {
		try {
			let postURL = this.serverURL + "api/usr/requeststate";
			let response = await axios.post(postURL, {
				roomid: roomId
			});
			let newRoomState = {
				'roomId': roomId,
				'power': that.$store.state.clientRoomState.power,
				'targetTemp': that.$store.state.clientRoomState.targetTemp,
				'targetWind': that.$store.state.clientRoomState.targetWind,
				'currentMode': that.$store.state.clientRoomState.currentMode,
				'currentTemp': response.data.currentTemp,
				'currentFee': response.data.currentFee,
				'totalFee': response.data.totalFee,
			};
			that.$store.commit('setClientRoomState', {'roomState': newRoomState});
			return response.data.error_code;
		} catch (e) {
			console.log(e);
			return -1;//network error
		}
	}

	/**
	 * 请求调温
	 * @param store
	 * @param roomId
	 * @param requestTargetTemp
	 * @returns {Promise<number>}
	 */
	async changeTargetTemp(store, roomId, requestTargetTemp) {
		try {
			let postURL = this.serverURL + "api/usr/changetargettemp";
			let response = await axios.post(postURL, {
				roomid: roomId,
				targetTemp: requestTargetTemp
			});
			if (response.data.error_code === 0) {
				let newRoomState = store.state.clientRoomState;
				newRoomState.targetTemp = requestTargetTemp;
				store.commit('setClientRoomState', {'roomState': newRoomState});
			}
			return response.data.error_code;
		} catch (e) {
			console.log(e);
			return -1;//network error
		}
	}

	/**
	 * 请求调风
	 * @param roomId
	 * @param requestFanSpeed
	 * @returns {Promise<number|*>}
	 */
	async changeTargetFanSpeed(roomId, requestFanSpeed) {
		try {
			let postURL = this.serverURL + "api/usr/changefanspeed";
			let response = await axios.post(postURL, {
				roomid: roomId,
				fanSpeed: requestFanSpeed
			});
			if (response.data.error_code === 0) {
				let newRoomState = store.state.clientRoomState;
				newRoomState.targetWind = requestFanSpeed;
				store.commit('setClientRoomState', {'roomState': newRoomState});
			}
			return response.data.error_code;
		} catch (e) {
			console.log(e);
			return -1;//network error
		}
	}

	/**
	 * 管理员部分
	 */
	/**
	 * 管理员开关服务器，这个实际上没用
	 * @param toPower
	 * @returns {Promise<number|*>}
	 */
	async setServerPower(toPower) {
		try {
			if (toPower === true) {
				let postURL = this.serverURL + "api/admin/poweron";
				let response = await axios.post(postURL);
				return response.data.error_code;
			} else {
				let postURL = this.serverURL + "api/admin/poweroff";
				let response = await axios.post(postURL);
				return response.data.error_code;
			}
		} catch (e) {
			console.log(e);
			return -1;//network error
		}
	}

	/**
	 * 设置中央空调工作模式
	 * @param mode 1致冷，-1制热 int
	 * @param maxTemp int
	 * @param minTemp int
	 * @param defaultTemp int
	 * @param defaultSpeed string
	 * @param highFeeRate 不通风速下的费率，float
	 * @param midFeeRate
	 * @param lowFeeRate
	 * @returns {Promise<number|*>}
	 */
	async setCACMode(mode, maxTemp, minTemp, defaultTemp, defaultSpeed, highFeeRate, midFeeRate, lowFeeRate) {
		try {
			let postURL = this.serverURL + "api/admin/setpara";
			let response = await axios.post(postURL, {
				mode: mode,
				temp_h: maxTemp,
				temp_l: minTemp,
				default_targetTemp: defaultTemp,
				default_fanSpeed: defaultSpeed,
				feeRate_h: highFeeRate,
				feeRate_m: midFeeRate,
				feeRate_l: lowFeeRate
			});
			return response.data.error_code;
		} catch (e) {
			console.log(e);
			return -1;//network error
		}
	}

	/**
	 * 开启中央空调
	 * @param toPower
	 * @returns {Promise<number|*>}
	 */
	async setCACPower(toPower) {
		try {
			if (toPower === true) {
				let postURL = this.serverURL + "api/admin/startup";
				let response = await axios.post(postURL);
				return response.data.error_code;
			} else {
				let postURL = this.serverURL + "api/admin/stop";
				let response = await axios.post(postURL);
				return response.data.error_code;
			}
		} catch (e) {
			console.log(e);
			return -1;//network error
		}
	}

	/**
	 * 管理员查看房间状态
	 * @returns {Promise<number|*>}
	 */
	async getRoomsState() {
		//TODO:接口有问题，不知道房间列表
		try {
			let postURL = this.serverURL + "api/admin/checkroomstate";
			let response = await axios.post(postURL);
			//todo 存储结果
			let roomStateList = response.data.data;
			for (let i = 0; i < Object.keys(roomStateList).length; i++) {
				// Vue.set(this.$store.state.roomInfo, 'invoice', response.data.data);
			}
			return response.data.error_code;
		} catch (e) {
			console.log(e);
			return -1;//network error
		}

	}

	/**
	 * 前台部分
	 */
	/**
	 * 打印详单
	 * @param roomId
	 * @returns {Promise<number|*>}
	 */
	async createInvoice(roomId) {
		try {
			let postURL = this.serverURL + "api/recp/createinvoice";
			let response = await axios.post(postURL, {
				roomid: roomId,
			});
			Vue.set(this.$store.state.roomInfo, 'invoice', response.data.data);
			return response.data.error_code;
		} catch (e) {
			console.log(e);
			return -1;//network error
		}
	}

	/**
	 * 经理部分
	 */
	/**
	 * 经理创建报表
	 * @param roomList
	 * @param beginDate
	 * @param endDate
	 * @returns {Promise<void>}
	 */
	async createReport(roomList, beginDate, endDate) {
		try {
			let postURL = this.serverURL + "api/mgr/createreport";
			let response = await axios.post(postURL, {
				list_RoomId: roomList,
				date1: beginDate,
				date2: endDate
			});
			let roomReports = response.data.data;
			for (let i = 0; i < roomReports.length; i++) {
				//todo
			}
			return response.data.error_code;
		} catch (e) {
			console.log(e);
			return -1;//network error
		}
	}


}