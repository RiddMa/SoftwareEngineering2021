<template>
	<div class="layout">
		<Header class="aHeader">
			<h2 class="aHeaderContent">
				酒店空调管理系统
				<Button shape="circle" type="primary" @click="addAC(defaultAC)">[测试用]添加空调</Button>
				<Button shape="circle" type="primary" @click="checkRoomsState()">[测试用]查看房间状态</Button>
				<Switch slot="extra" v-model="this.isPolling" shape="circle" size="large" type="primary"
				        @on-change="handlePollingSwitch()">
					<span slot="open">ON</span>
					<span slot="close">OFF</span>
				</Switch>

			</h2>
			<Menu active-name="1" class="aMenu" mode="horizontal">
				<MenuItem name="1" to="/admin/main">
					<Icon type="ios-apps"></Icon>
					<span class="MenuText">空调概览</span>
				</MenuItem>
				<MenuItem name="2" to="/admin/search">
					<Icon type="ios-search"></Icon>
					<span class="MenuText">房间查询</span>
				</MenuItem>
				<MenuItem name="3" to="/admin/settings">
					<Icon type="ios-settings"></Icon>
					<span class="MenuText">偏好设置</span>
				</MenuItem>
			</Menu>
		</Header>
		<Content :style="{padding:'0 5vw 0 5vw'}">
			<div :style="{padding: '60px'}"></div>
			<keep-alive>
				<router-view></router-view>
			</keep-alive>
		</Content>
	</div>
</template>

<script>
import Vue from "vue";
import random_str from "view-design/src/utils/random_str";
import util from "../../libs/util";
import {NetworkController} from "../../libs/NetworkController";

export default {
	name: 'admin',
	data() {
		return {
			activeTab: '1',
			isPolling: false,
			polling: null,
		};
	},
	methods: {
		/**
		 * 向 Vuex 注册空调
		 * @param acInfo
		 */
		addAC: function (acInfo) {
			Vue.set(this.$store.state.roomInfo, acInfo.rid, acInfo);
			console.log(this.$store.state);
		},
		handlePollingSwitch() {
			if (this.isPolling === true) {
				this.isPolling = false;
				clearInterval(this.polling);
				console.log('Stop polling');
			} else {
				this.isPolling = true;
				this.polling = setInterval(() => {
					this.getAdminRoomState();
				}, 5000);
				console.log('Start polling');
			}
		},
		async getAdminRoomState() {
			let nc = NetworkController.getInstance();
			let response = await nc.getRoomsState();
			console.log('Polled');
		}
	},
}
</script>

<style scoped src="../../styles/header.css"></style>
<style scoped>

</style>
