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
							<Switch v-model="thisRoom.power" shape="circle" size="large" type="primary"
							        @on-change="handlePowerSwitch()">
								<span slot="open">ON</span>
								<span slot="close">OFF</span>
							</Switch>
						</Col>
					</Row>

					<div v-if="thisRoom.power" class="acStateInfo">
						<Row class="acCardContent">
							<Col :span="12">
								<span class="acCardContentText">当前温度：</span>
							</Col>
							<Col :span="12">
								<Row>
									<Col :span="8" align="middle" class="acCardContentText">
										<Button icon="ios-arrow-down" shape="circle" size="large"
										        @click="changeTemp($event,-1)"></Button>
									</Col>
									<Col :span="8" align="middle">
										<span class="digitFont">{{ this.thisRoom.targetTemp }}</span>
									</Col>
									<Col :span="8" align="middle">
										<Button class="acCardContentText" icon="ios-arrow-up" shape="circle" size="large"
										        @click="changeTemp($event,1)"></Button>
									</Col>
								</Row>
							</Col>
						</Row>

						<Row class="acCardContent">
							<Col :span="12">
								<span class="acCardContentText">当前风速：</span>
							</Col>
							<Col :span="12" class="acCardContentText">
								<Row>
									<Col :span="8" align="middle">
										<Button icon="md-remove" shape="circle" size="large"
										        @click="changeWind($event,-1)"></Button>
									</Col>
									<Col :span="8" align="middle">
										<span class="digitFont">{{ this.thisRoom.targetWind }}</span>
									</Col>
									<Col :span="8" align="middle">
										<Button icon="md-add" shape="circle" size="large"
										        @click="changeWind($event,1)"></Button>
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
										<Button v-if="thisRoom.currentMode==='致冷'" icon="ios-snow" shape="circle" size="large"
										        type="primary"
										        @click="changeMode($event,'致冷')"></Button>
										<Button v-else icon="ios-snow" shape="circle" size="large"
										        @click="changeMode($event,'致冷')"></Button>
									</Col>
									<Col :span="8" align="middle">
										<span style="vertical-align: middle">{{ thisRoom.currentMode }}</span>
									</Col>
									<Col :span="8" align="middle">
										<Button v-if="thisRoom.currentMode==='制热'" icon="ios-sunny" shape="circle" size="large"
										        type="primary"
										        @click="changeMode($event,'制热')"></Button>
										<Button v-else icon="ios-sunny" shape="circle" size="large"
										        @click="changeMode($event,'制热')"></Button>
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
			title: null,
			thisRoom: this.$store.state.clientRoomState,
			polling: null,
			networkController: NetworkController.getInstance(),
		}
	},
	methods: {
		async handlePowerSwitch() {
			let nc = NetworkController.getInstance()
			if (this.thisRoom.power === true) {
				console.log(this.thisRoom);
				await nc.setUserPower(this, this.thisRoom.roomId, true);
			} else {
				await nc.setUserPower(this, this.thisRoom.roomId, false);
			}
		},
		/**
		 * 空调温度控制
		 * @param event
		 * @param turnUp 升高的温度值，取值+1、-1
		 */
		async changeTemp(event, turnUp) {
			let requestTargetTemp = this.thisRoom.targetTemp + turnUp;
			let nc = NetworkController.getInstance();
			if (util.validateTemp(requestTargetTemp) === true) {
				await nc.changeTargetTemp(this.$store, this.thisRoom.roomId, requestTargetTemp);
			} else {
				//no-op
			}
		},
		/**
		 * 空调风速控制
		 * @param event
		 * @param turnUp 升高的风速档位，取值+1、-1
		 */
		async changeWind(event, turnUp) {
			let targetWind = this.thisRoom.targetWind + turnUp;
			let nc = NetworkController.getInstance();
			if (util.validateWind(targetWind) === true) {
				await nc.changeTargetFanSpeed(this.thisRoom.roomId, targetWind);
				this.thisRoom.targetWind = targetWind;
			} else {
				//no-op
			}
			console.log(this.thisRoom.targetWind);

		},
		/**
		 * 空调模式控制
		 * @param event
		 * @param toMode 目标模式，取值 致冷、制热
		 */
		changeMode: function (event, toMode) {
			this.thisRoom.currentMode = toMode;
			//TODO:目前还没有这个功能
		},
		pollClientRoomState() {
			this.polling = setInterval(async () => {
				let errCode = await this.networkController.heartBeat(this, this.thisRoom.roomId);
				console.log('Polled');
			}, 5000);
		}

	},
	created() {
		if (this.thisRoom === null) {
			this.$router.push({path: '/client/login'});
		}
		this.pollClientRoomState();
	},
	beforeDestroy() {
		clearInterval(this.polling);
	},

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