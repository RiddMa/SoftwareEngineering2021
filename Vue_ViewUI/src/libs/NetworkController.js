import axios from "axios";
import Vue from "vue";
import store from "./store";
import moment from "moment-timezone";

/**
 * 使用getInstance()方法获取唯一实例
 */
export class NetworkController {
	constructor() {
		this.serverURL = "http://10.128.209.242:5000/";
		this.useToken = false;
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
			if (response.data.error_code === 0) {
				let roomState = {
					'roomId': roomId,
					'power': false,
					'targetTemp': 24,
					'targetWind': 2,
					'currentMode': '致冷',
					'currentTemp': response.data.data.currentTemp,
					'currentFee': 0.0,
					'totalFee': 0.0,
				};
				that.$store.commit('setClientRoomState', {roomState: roomState});
				that.$store.commit('setToken', {'userType': 0, 'token': response.data.data.token});
			}
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
				if (this.useToken) {
					that.$store.commit('setToken', {'userType': userType, 'token': response.data.data.token});
				}
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
	 * @param operator
	 * @returns {Promise<*>}
	 */
	async setUserPower(that, roomId, toPower, operator = 0) {
		let response;
		switch (operator) {
			case 0: {
				let newRoomState = that.$store.state.clientRoomState;
				if (toPower === true) {
					try {
						let postURL = this.serverURL + "api/usr/poweron";
						response = await axios.post(postURL, {
							roomId: roomId,
							targetTemp: newRoomState.targetTemp,
							fanSpeed: (newRoomState.targetWind - 1).toString(),
							currentTemp: newRoomState.currentTemp,
						});
					} catch (e) {
						console.log(e);
						return -1;//network error
					}
				} else {
					try {
						let postURL = this.serverURL + "api/usr/poweroff";
						response = await axios.post(postURL, {
							roomId: roomId
						});
					} catch (e) {
						console.log(e);
						return -1;//network error
					}
				}
				if (response.error_code === 0) {
					newRoomState.power = toPower;
					that.$store.commit('setClientRoomState', {'roomState': newRoomState});
				}
				return response.error_code;
			}
			case 1: {
				let targetRoomIndex = that.$store.state.adminRoomState.findIndex(item => {
					return item.roomId === roomId;
				});
				if (targetRoomIndex !== -1) {
					let targetRoomState = that.$store.state.adminRoomState[targetRoomIndex];
					if (toPower === true) {
						try {
							console.log('send');
							let postURL = this.serverURL + "api/usr/poweron";
							response = await axios.post(postURL, {
								roomId: roomId,
								targetTemp: targetRoomState.targetTemp,
								fanSpeed: (targetRoomState.targetWind - 1).toString(),
								currentTemp: targetRoomState.currentTemp,
							});
						} catch (e) {
							console.log(e);
							return -1;//network error
						}
					} else {
						try {
							let postURL = this.serverURL + "api/usr/poweroff";
							response = await axios.post(postURL, {
								roomId: roomId
							});
						} catch (e) {
							console.log(e);
							return -1;//network error
						}
					}
					if (response.error_code === 0) {
						targetRoomState.power = toPower;
						that.$store.commit('setAdminRoomState', targetRoomState);
					}
					return response.error_code;
				}
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
				roomId: roomId
			});
			let newRoomState = {
				'roomId': roomId,
				'power': that.$store.state.clientRoomState.power,
				'targetTemp': that.$store.state.clientRoomState.targetTemp,
				'targetWind': that.$store.state.clientRoomState.targetWind,
				'currentMode': that.$store.state.clientRoomState.currentMode,
				'currentTemp': response.data.data.currentTemp,
				'currentFee': response.data.data.currentFee,
				'totalFee': response.data.data.totalFee,
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
	 * @param that
	 * @param roomId
	 * @param requestTargetTemp
	 * @param operator
	 * @returns {Promise<number>}
	 */
	async changeTargetTemp(that, roomId, requestTargetTemp, operator = 0) {
		try {
			let postURL = this.serverURL + "api/usr/changetargettemp";
			let response = await axios.post(postURL, {
				roomId: roomId,
				targetTemp: requestTargetTemp
			});
			if (response.data.error_code === 0) {
				switch (operator) {
					case 0: {
						that.$store.commit('setClientTargetTemp', requestTargetTemp);
						break;
					}
					case 1: {
						let targetRoomIndex = that.$store.state.adminRoomState.findIndex(item => {
							return item.roomId === roomId;
						})
						if (targetRoomIndex !== -1) {
							let newRoomState = that.$store.state.adminRoomState[targetRoomIndex];
							newRoomState.targetTemp = requestTargetTemp;
							that.$store.commit('setAdminRoomState', newRoomState);
						}
					}
				}
			}
			return response.data.error_code;
		} catch (e) {
			console.log(e);
			return -1;//network error
		}
	}

	/**
	 * 请求调风
	 * @param that
	 * @param roomId
	 * @param requestFanSpeed
	 * @param operator
	 * @returns {Promise<number|*>}
	 */
	async changeTargetFanSpeed(that, roomId, requestFanSpeed, operator = 0) {
		try {
			let postURL = this.serverURL + "api/usr/changefanspeed";
			let response = await axios.post(postURL, {
				roomId: roomId,
				fanSpeed: (requestFanSpeed - 1).toString()
			});
			if (response.data.error_code === 0) {
				switch (operator) {
					case 0: {
						that.$store.commit('setClientTargetWind', requestFanSpeed);
						break;
					}
					case 1: {
						let targetRoomIndex = that.$store.state.adminRoomState.findIndex(item => {
							return item.roomId === roomId;
						})
						if (targetRoomIndex !== -1) {
							let newRoomState = that.$store.state.adminRoomState[targetRoomIndex];
							newRoomState.targetWind = requestFanSpeed;
							that.$store.commit('setAdminRoomState', newRoomState);
						}
					}
				}
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
				let response = await axios.post(postURL,{});
				return response.data.error_code;
			} else {
				let postURL = this.serverURL + "api/admin/poweroff";
				let response = await axios.post(postURL,{});
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
				let response = await axios.post(postURL,{});
				return response.data.error_code;
			} else {
				let postURL = this.serverURL + "api/admin/stop";
				let response = await axios.post(postURL,{});
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
	async getRoomsState(that) {
		try {
			let postURL = this.serverURL + "api/admin/checkroomstate";
			let response = await axios.post(postURL,{});
			let roomStateList = response.data.data;
			that.$store.commit('setAdminAllRoomState', roomStateList);
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
	 * 打印账单
	 * @param that
	 * @param roomId
	 * @returns {Promise<number|*>}
	 */
	async createInvoice(that, roomId) {
		try {
			let postURL = this.serverURL + "api/recp/createinvoice";
			let response = await axios.post(postURL, {
				roomId: roomId,
			});
			let invoiceData = [{
				roomId: response.data.data.RoomId,
				totalFee: response.data.data.Total_Fee,
				dateIn: response.data.data.date_in,
				dateOut: response.data.data.date_out,
			}];
			that.$store.commit('setInvoice', invoiceData);
			return response.data.error_code;
		} catch (e) {
			console.log(e);
			return -1;//network error
		}
	}

	/**
	 *
	 * @param that
	 * @param roomId
	 * @returns {Promise<number>}
	 */
	async createDetailedList(that, roomId) {
		try {
			let postURL = this.serverURL + "api/recp/createrd";
			let response = await axios.post(postURL, {
				roomId: roomId,
			});
			let detailedList = [];
			console.log(response.data.data)
			for (let i = 0; i < response.data.data.length; i++) {
				detailedList[i] = {
					roomId: response.data.data[i].RoomId,
					requestTime: response.data.data[i].RequestTime,
					requestDuration: response.data.data[i].RequestDuration,
					fanSpeed: response.data.data[i].FanSpeed,
					feeRate: response.data.data[i].FeeRate,
					fee: response.data.data[i].Fee
				};
			}
			that.$store.commit('setDetailedList', detailedList);
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
	 * @param that
	 * @param roomList
	 * @param queryDateRange
	 * @returns {Promise<number>}
	 */
	async createReport(that, roomList, queryDateRange) {
		try {
			let postURL = this.serverURL + "api/mgr/createreport";
			let response = await axios.post(postURL, {
				roomId: roomList,
				date1: moment(queryDateRange[0]).format('YYYY-MM-DD HH:mm:ss'),
				date2: moment(queryDateRange[1]).format('YYYY-MM-DD HH:mm:ss'),
			});
			let roomReports = [];
			console.log(response.data.data)
			for (let i = 0; i < response.data.data.length; i++) {
				roomReports[i] = {
					roomId: response.data.data[i].roomId,
					changeTempTimes: response.data.data[i].changetemptimes,
					changeSpeedTimes: response.data.data[i].changespeedtimes,
					totalFee: response.data.data[i].totalfee,
					powerOffTimes: response.data.data[i].powerofftimes,
					detailedListNum: response.data.data[i].DRnum,
					acWorkingTime: response.data.data[i].ACworkingtime
				};
			}
			that.$store.commit('setManagerReport', roomReports);
			return response.data.error_code;
		} catch (e) {
			console.log(e);
			return -1;//network error
		}
	}
}