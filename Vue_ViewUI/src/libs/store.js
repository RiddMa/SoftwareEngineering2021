import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
	state: {
		centralAirCon: false,//centralAirCon for Central Air-Conditioning
		username: '',
		userToken: '',
		adminToken: '',
		receptionToken: '',
		managerToken: '',
		invoice: [],
		detailedList: [],
		managerReport: [],
		clientRoomState: null,
		adminRoomState: null,
	},
	getters: {},
	mutations: {
		/**
		 * 设置中央空调状态
		 * @param state Vuex的状态变量，commit无需传入
		 * @param toPower 目标状态
		 */
		setCAC(state, {toPower}) {
			state.centralAirCon = toPower;
		},
		/**
		 *
		 * @param state
		 * @param username
		 */
		setUsername(state, {username}) {
			state.username = username;
		},
		/**
		 *
		 * @param state Vuex的状态变量，commit无需传入
		 * @param userType 0-客户，1-管理员，2-前台，3-经理
		 * @param token token
		 */
		setToken(state, {userType, token}) {
			switch (userType) {
				case 0:
					state.userToken = token;
					break;
				case 1:
					state.adminToken = token;
					break;
				case 2:
					state.receptionToken = token;
					break;
				case 3:
					state.managerToken = token;
					break;
			}
		},
		/**
		 * 仅在客户端调用
		 * @param state Vuex的状态变量，commit无需传入
		 * @param roomState 房间对象
		 */
		setClientRoomState(state, {roomState}) {
			state.clientRoomState = roomState;
		},
		setClientPower(state, power) {
			state.clientRoomState.power = power;
		},
		setClientTargetTemp(state, targetTemp) {
			state.clientRoomState.targetTemp = targetTemp;
		},
		setClientTargetWind(state, targetWind) {
			state.clientRoomState.targetWind = targetWind;
		},
		setClientCurrentMode(state, currentMode) {
			state.clientRoomState.currentMode = currentMode;
		},
		setClientCurrentTemp(state, currentTemp) {
			state.clientRoomState.currentTemp = currentTemp;
		},
		setClientCurrentFee(state, currentFee) {
			state.clientRoomState.currentFee = currentFee;
		},
		setClientTotalFee(state, totalFee) {
			state.clientRoomState.totalFee = totalFee;
		},
		/**
		 *
		 * @param state Vuex的状态变量，commit无需传入
		 * @param roomState 房间对象
		 */
		setAdminRoomState(state, roomState) {
			if (state.adminRoomState === null) {
				state.adminRoomState = [];
			}
			let targetRoomIndex = state.adminRoomState.findIndex(item => {
				return item.roomId === roomState.roomId;
			})
			if (targetRoomIndex === -1) {
				state.adminRoomState.push(roomState);
			} else {
				Vue.set(state.adminRoomState, targetRoomIndex, roomState);
			}
		},
		/**
		 * 管理员轮询
		 * @param state
		 * @param roomStateList
		 */
		setAdminAllRoomState(state, roomStateList) {
			state.adminRoomState = [];
			for (let i = 0; i < roomStateList.length; i++) {
				roomStateList[i].fanSpeed = (parseInt(roomStateList[i].fanSpeed) + 1);
				state.adminRoomState.push(roomStateList[i]);
			}
		},
		/**
		 * 前台
		 */
		/**
		 * 设置账单
		 * @param state
		 * @param invoiceItem
		 */
		setInvoice(state, invoiceItem) {
			Vue.set(state, 'invoice', invoiceItem);
		},
		/**
		 * 设置详单
		 * @param state
		 * @param detailedList 详单
		 */
		setDetailedList(state, detailedList) {
			Vue.set(state, 'detailedList', detailedList);
		},
		setManagerReport(state, roomReports) {
			Vue.set(state, 'managerReport', roomReports);
		},
	},
	actions: {},
})