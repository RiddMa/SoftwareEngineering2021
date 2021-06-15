<template>
	<div>
		<Row align="middle" justify="center" type="flex">

			<Col :lg="13" :md="15" :sm="18" :xl="10" :xs="22" :xxl="8">
				<Card class="CtrlPanel">
					<h1 slot="title" class="titleHeader">用户刷卡</h1>
					<Input v-model="roomId" class="CtrlGroup" clearable placeholder="请输入房间号" size="large"></Input>
					<br>
					<Input v-model="password" class="CtrlGroup" password placeholder="请输入密码" size="large" type="password"/>
					<br>
					<Button class="CtrlGroup" shape="circle" size="large" type="primary" @click="userLogin($event)">登录</Button>
				</Card>
			</Col>
		</Row>

	</div>

</template>

<script>
import {NetworkController} from "../../libs/NetworkController.js";
import Vue from "vue";
import random_str from "view-design/src/utils/random_str";

export default {
	name: "ClientLogin",
	data: function () {
		return {
			roomId: '',
			password: ''
		}
	},
	methods: {
		/**
		 * 向Vuex注册用户
		 * @param roomId
		 */
		addDefaultRoom2Vuex(roomId) {
			let roomState = {
				'roomId': roomId,
				'power': false,
				'targetTemp': 24,
				'targetWind': 2,
				'currentMode': '致冷',
				'currentTemp': 26,
				'currentFee': 0.0,
				'totalFee': 0.0,
			};
			this.$store.commit('setClientRoomState', {roomState: roomState});
		},
		/**
		 * 用户登录
		 * @param event
		 */
		async userLogin(event) {
			let nc = NetworkController.getInstance();
			let errCode = await nc.enterRoom(this, this.roomId, this.password);
			if (errCode === 0) {
				// this.addDefaultRoom2Vuex(this.roomId);
				this.$router.push({path: '/client'});// route to client view
			} else if (errCode === 1) {
				//TODO:login failed
				// this.$router.push({path: '/client'});// route to client view
			} else if (errCode === -1) {
				//TODO:network error
				this.addDefaultRoom2Vuex(this.roomId);
				this.$router.push({path: '/client'});// route to client view
			}
		},
	}
}
</script>

<style scoped>
.CtrlPanel {
	max-width: 700px;
	margin: 15vh auto 25vh;
	text-align: center;
}

.CtrlGroup {
	margin: 2vh auto;
	max-width: 400px;
	font-size: large;
}

.titleHeader {
	margin-top: 2vh;
	margin-bottom: 2vh;
}
</style>