import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
	state: {
		CAC: false,//CAC for Central Air-Conditioning
		username: '',
		userToken: '',
		adminToken: '',
		receptionToken: '',
		managerToken: '',
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
			state.CAC = toPower;
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
		/**
		 *
		 * @param state Vuex的状态变量，commit无需传入
		 */
		initAdminRoomState(state) {
			state.adminRoomState = {};
		},
		/**
		 *
		 * @param state Vuex的状态变量，commit无需传入
		 * @param roomState 房间对象
		 */
		setAdminRoomState(state, {roomState}) {
			if (state.adminRoomState === null) {
				state.adminRoomState = {};
			}
			let roomId = roomState.roomId;
			state.adminRoomState[roomId] = roomState;
		},


	},
	actions: {},
})