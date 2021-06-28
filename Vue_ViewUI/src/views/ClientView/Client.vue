<template>
	<div class="index">
		<Row align="middle" justify="center" type="flex">
			<Col :lg="13" :md="15" :sm="18" :xl="10" :xs="20">
				<Card class="CtrlPanel">
					<h1 slot="title" class="CardTitle">
						<img src="../../images/logo.png">
					</h1>
					<h2 slot="title" class="CardTitle">空调状态</h2>

					<Row class="acCardContent">
						<Col :span="12">
							<span class="acCardContentText">当前状态：</span>
						</Col>
						<Col :span="12" align="middle" class="acCardContentText">
							<Switch v-model="power" shape="circle" size="large" type="primary"
							        @on-change="handlePowerSwitch()">
								<span slot="open">ON</span>
								<span slot="close">OFF</span>
							</Switch>
						</Col>
					</Row>
					<Row class="acCardContent">
						<Col :span="12">
							<span class="acCardContentText">当前费用：</span>
						</Col>
						<Col :span="12" align="middle" class="acCardContentText">
							<span class="acCardContentText">￥{{ currentFee }}</span>
						</Col>
					</Row>
					<Row class="acCardContent">
						<Col :span="12">
							<span class="acCardContentText">总计费用：</span>
						</Col>
						<Col :span="12" align="middle" class="acCardContentText">
							<span class="acCardContentText">￥{{ totalFee }}</span>
						</Col>
					</Row>

					<div v-if="power" class="acStateInfo">
						<Row class="acCardContent">
							<Col :span="12">
								<span class="acCardContentText">目标温度：</span>
							</Col>
							<Col :span="12">
								<Row>
									<Col :span="8" align="middle" class="acCardContentText">
										<Button icon="ios-arrow-down" shape="circle" size="large"
										        @click="changeTemp(-1)"></Button>
									</Col>
									<Col :span="8" align="middle">
										<span class="digitFont">{{ targetTemp }}</span>
									</Col>
									<Col :span="8" align="middle">
										<Button class="acCardContentText" icon="ios-arrow-up" shape="circle" size="large"
										        @click="changeTemp(1)"></Button>
									</Col>
								</Row>
							</Col>
						</Row>

						<Row class="acCardContent">
							<Col :span="12">
								<span class="acCardContentText">目标风速：</span>
							</Col>
							<Col :span="12" class="acCardContentText">
								<Row>
									<Col :span="8" align="middle">
										<Button icon="md-remove" shape="circle" size="large"
										        @click="changeWind(-1)"></Button>
									</Col>
									<Col :span="8" align="middle">
										<span class="digitFont">{{ targetWind }}</span>
									</Col>
									<Col :span="8" align="middle">
										<Button icon="md-add" shape="circle" size="large"
										        @click="changeWind(1)"></Button>
									</Col>
								</Row>
							</Col>
						</Row>

						<Row class="acCardContent">
							<Col :span="12" class="acCardContentText">
								<span>当前模式：</span>
							</Col>
							<Col :span="12" class="acCardContentText">
								<Row>
									<Col :span="8" align="middle">
										<Button v-if="currentMode==='致冷'" icon="ios-snow" shape="circle"
										        size="large"
										        type="primary"
										        @click="changeMode('致冷')"></Button>
										<Button v-else icon="ios-snow" shape="circle" size="large"
										        @click="changeMode('致冷')"></Button>
									</Col>
									<Col :span="8" align="middle">
										<span style="vertical-align: middle">{{ currentMode }}</span>
									</Col>
									<Col :span="8" align="middle">
										<Button v-if="currentMode==='制热'" icon="ios-sunny" shape="circle"
										        size="large"
										        type="primary"
										        @click="changeMode('制热')"></Button>
										<Button v-else icon="ios-sunny" shape="circle" size="large"
										        @click="changeMode('制热')"></Button>
									</Col>
								</Row>
							</Col>
						</Row>
					</div>
					<div v-else class="acStateInfo"></div>
				</Card>
			</Col>
			<col flex="auto"></col>
		</Row>
	</div>
</template>
<script>
import Vue from "vue";
import util from "../../libs/util";
import {NetworkController} from "../../libs/NetworkController";

export default {
	name: 'Client',
	data: function () {
		return {
			roomId: this.$store.state.clientRoomState.roomId,
			title: null,
			polling: null,
			networkController: NetworkController.getInstance(),
		}
	},
	computed: {
		power: {
			get: function () {
				return this.$store.state.clientRoomState.power;
			},
			set: function (newState) {
				this.$store.commit('setClientPower', newState);
			},
		},
		targetTemp: {
			get: function () {
				return this.$store.state.clientRoomState.targetTemp;
			},
			set: function (newState) {
				this.$store.commit('setClientTargetTemp', newState);
			},
		},
		targetWind: {
			get: function () {
				return this.$store.state.clientRoomState.targetWind;
			},
			set: function (newState) {
				this.$store.commit('setClientTargetWind', newState);
			},
		},
		currentMode: {
			get: function () {
				return this.$store.state.clientRoomState.currentMode;
			},
			set: function (newState) {
				this.$store.commit('setClientCurrentMode', newState);
			},
		},
		currentTemp: {
			get: function () {
				return this.$store.state.clientRoomState.currentTemp;
			},
			set: function (newState) {
				this.$store.commit('setClientCurrentTemp', newState);
			},
		},
		currentFee: {
			get: function () {
				return this.$store.state.clientRoomState.currentFee;
			},
			set: function (newState) {
				this.$store.commit('setClientCurrentFee', newState);
			},
		},
		totalFee: {
			get: function () {
				return this.$store.state.clientRoomState.totalFee;
			},
			set: function (newState) {
				this.$store.commit('setClientTotalFee', newState);
			},
		},
	},
	methods: {
		async handlePowerSwitch() {
			let nc = NetworkController.getInstance();
			if (this.power === true) {
				await nc.setUserPower(this, this.roomId, true);
				this.pollClientRoomState();
			} else {
				await nc.setUserPower(this, this.roomId, false);
				clearInterval(this.polling);
			}
		},
		/**
		 * 空调温度控制
		 * @param turnUp 升高的温度值，取值+1、-1
		 */
		async changeTemp(turnUp) {
			let requestTargetTemp = this.targetTemp + turnUp;
			let nc = NetworkController.getInstance();
			if (util.validateTemp(requestTargetTemp) === true) {
				await nc.changeTargetTemp(this, this.roomId, requestTargetTemp);
			} else {
				//no-op
			}
		},
		/**
		 * 空调风速控制
		 * @param turnUp 升高的风速档位，取值+1、-1
		 */
		async changeWind(turnUp) {
			let targetWind = this.targetWind + turnUp;
			let nc = NetworkController.getInstance();
			if (util.validateWind(targetWind) === true) {
				await nc.changeTargetFanSpeed(this, this.roomId, targetWind);
			} else {
				//no-op
			}
		},
		/**
		 * 空调模式控制
		 * @param event
		 * @param toMode 目标模式，取值 致冷、制热
		 */
		changeMode: function (toMode) {
			this.currentMode = toMode;
			//TODO:目前还没有这个功能
		},
		pollClientRoomState() {
			this.polling = setInterval(async () => {
				let errCode = await this.networkController.heartBeat(this, this.roomId);
				console.log('Polled');
			}, 5000);
		}

	},
	created() {
		if (this.$store.state.clientRoomState === null) {
			this.$router.push({path: '/client/login'});
		}
	},
	// beforeDestroy() {
	//
	// },

}
</script>

<style scoped src="../../styles/client.css"></style>
<style scoped lang="less">
.index {
	width: 100%;
	margin-top: 5vh;
	margin-bottom: 5vh;
	//text-align: center;
	font-size: x-large;

	h1 {
		height: 100px;
	}

	h2 {
		text-align: center;
		margin-top: 1vh;
		margin-bottom: 1vh;

		p {
			margin: 0 0 1vh;
		}
	}

	.ivu-row-flex {
		height: 100%;
	}
}

.CtrlPanel {
	margin-top: 5vh;
	margin-bottom: 5vh;
	//font-size: xx-large;
}

.CardTitle {
	font-size: xx-large;
}

.CardTitle img {
	max-width: 100%;
	max-height: 100%;
	display: block;
	margin: auto;
}

.CtrlGroup {
	margin-top: 1vh;
	margin-bottom: 1vh;
}

.digitFont {
	font-family: Digital7-mono;
	font-size: xx-large;
	vertical-align: middle;
}
</style>