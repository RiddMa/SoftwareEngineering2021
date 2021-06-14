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
							<Switch v-model="thisRoom.power" shape="circle" size="large" type="primary" @on-change="handleSwitch()">
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
										<span class="digitFont">{{ this.thisRoom.curnTemp }}</span>
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
										<span class="digitFont">{{ this.thisRoom.curnWind }}</span>
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
										<Button v-if="thisRoom.curnMode==='致冷'" icon="ios-snow" shape="circle" size="large" type="primary"
										        @click="changeMode($event,'致冷')"></Button>
										<Button v-else icon="ios-snow" shape="circle" size="large"
										        @click="changeMode($event,'致冷')"></Button>
									</Col>
									<Col :span="8" align="middle">
										<span style="vertical-align: middle">{{ thisRoom.curnMode }}</span>
									</Col>
									<Col :span="8" align="middle">
										<Button v-if="thisRoom.curnMode==='制热'" icon="ios-sunny" shape="circle" size="large" type="primary"
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

				<!--        <Card class="CtrlPanel">-->
				<!--          <h2 class="CardTitle" slot="title">控制面板</h2>-->
				<!--          <Switch class="CardTitle" slot="title" size="large" v-model="acSwitch" @on-change="handleSwitch">-->
				<!--            <span slot="open">ON</span>-->
				<!--            <span slot="close">OFF</span>-->
				<!--          </Switch>-->
				<!--          <h3>-->
				<!--            <ButtonGroup class="CtrlGroup" size="large" shape="circle">-->
				<!--              <Button type="primary" :disabled="acDisabled" @click="changeTemp($event,-1)">-->
				<!--                <Icon type="ios-arrow-down"></Icon>-->
				<!--                温度减-->
				<!--              </Button>-->
				<!--              <Button type="primary" :disabled="acDisabled" @click="changeTemp($event,1)">-->
				<!--                温度加-->
				<!--                <Icon type="ios-arrow-up"></Icon>-->
				<!--              </Button>-->
				<!--            </ButtonGroup>-->
				<!--            <br>-->
				<!--            <ButtonGroup class="CtrlGroup" size="large" shape="circle">-->
				<!--              <Button type="primary" :disabled="acDisabled" @click="changeWind($event,-1)">-->
				<!--                <Icon type="md-remove"></Icon>-->
				<!--                风速减-->
				<!--              </Button>-->
				<!--              <Button type="primary" :disabled="acDisabled" @click="changeWind($event,1)">-->
				<!--                风速加-->
				<!--                <Icon type="md-add"></Icon>-->
				<!--              </Button>-->
				<!--            </ButtonGroup>-->
				<!--            <br>-->
				<!--            <ButtonGroup class="CtrlGroup" size="large" shape="circle">-->
				<!--              <Button type="primary" :disabled="acDisabled" @click="changeMode($event,'致冷')">-->
				<!--                <Icon type="ios-snow"></Icon>-->
				<!--                致冷-->
				<!--              </Button>-->
				<!--              <Button type="primary" :disabled="acDisabled" @click="changeMode($event,'制热')">-->
				<!--                制热-->
				<!--                <Icon type="ios-sunny"></Icon>-->
				<!--              </Button>-->
				<!--            </ButtonGroup>-->
				<!--          </h3>-->
				<!--        </Card>-->
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
			thisRoom: this.$store.state.roomInfo[Object.keys(this.$store.state.roomInfo)[0]],
		}
	},
	methods: {

		async handleSwitch() {
			let nc = NetworkController.getInstance()
			if (this.thisRoom.power === true) {
				console.log(this.thisRoom);
				await nc.toggleUserPower(this.thisRoom.roomId, true);
			} else {
				await nc.toggleUserPower(this.thisRoom.roomId, false);
			}

			// this.acDisabled = !status;
			// //TODO:传入用户名
			// if (status === true) {
			//   console.log(turnonoff_u('testOnly', 1));
			// } else {
			//   console.log(turnonoff_u('testOnly', 0));
			// }
		},
		/**
		 * 空调温度控制
		 * @param event
		 * @param turnUp 升高的温度值，取值+1、-1
		 */
		async changeTemp(event, turnUp) {
			let targetTemp = this.thisRoom.targetTemp + turnUp;
			let nc = NetworkController.getInstance();
			if (util.validateTemp(targetTemp) === true) {
				await nc.changeTargetTemp(this.thisRoom.roomId, targetTemp);
				this.thisRoom.targetTemp = targetTemp;
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
			this.thisRoom.curnMode = toMode;
			//TODO:目前还没有这个功能
		}

	}
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