import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
	state: {
		CAC: false,//CAC for Central Air-Conditioning
		userToken: '',
		adminToken: '',
		receptionToken: '',
		managerToken: '',
	},
	getters: {},
	mutations: {
		/**
		 *
		 * @param state
		 * @param toPower
		 */
		setCAC(state, {toPower}) {
			state.CAC = toPower;
		},
		/**
		 *
		 * @param state
		 * @param userType 0-客户，1-管理员，2-前台，3-经理
		 * @param token
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
		 * @param state
		 * @param roomInfo
		 */
		setClientRoomState(state, {roomState}) {
			state.clientRoomState = roomState;
		},

		initAdminRoomState(state) {
			state.adminRoomState = {};
		},
		setAdminRoomState(state, {roomState}) {
			if (state.adminRoomState === undefined) {
				state.adminRoomState = {};
			}
			let roomId = roomState.roomId;
			state.adminRoomState.roomId = roomState;
		},


	},
	actions: {},
})