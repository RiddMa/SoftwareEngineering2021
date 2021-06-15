<template>
	<div>
		<Breadcrumb :style="{margin: '16px  1%'}">
			<BreadcrumbItem>管理员</BreadcrumbItem>
			<BreadcrumbItem>设置</BreadcrumbItem>
		</Breadcrumb>
		<Card>
			<Row>
				<Col :lg="10" :md="12" :sm="16" :xl="8" :xs="24" :xxl="6">
					<CellGroup>
						<Cell class="settings" title="中央空调控制">
							<Switch slot="extra" v-model="CAC" :before-change="handleBeforeSetCAC"
							        shape="circle" size="large" type="primary" @on-change="handleSetCAC">
								<span slot="open">ON</span>
								<span slot="close">OFF</span>
							</Switch>
						</Cell>
						<Cell class="settings" title="模式">
							<Switch slot="extra" v-model="CACMode" shape="circle" size="large" type="primary">
								<span slot="open">冷</span>
								<span slot="close">热</span>
							</Switch>
						</Cell>
						<Cell class="settings" title="最小温度">
							<Input slot="extra" v-model="minTemp" placeholder="Enter something..."/>
						</Cell>
						<Cell class="settings" title="最大温度">
							<Input slot="extra" v-model="maxTemp" placeholder="Enter something..."/>
						</Cell>
						<Cell class="settings" title="默认温度">
							<Input slot="extra" v-model="defaultTemp" placeholder="Enter something..."/>
						</Cell>
						<Cell class="settings" title="默认风速">
							<Input slot="extra" v-model="defaultFanSpeed" placeholder="Enter something..."/>
						</Cell>
						<Cell class="settings" title="管理员登出">
							<Button slot="extra" shape="circle" type="error" @click="adminLogout()">登出</Button>
						</Cell>
					</CellGroup>
				</Col>
			</Row>
		</Card>
	</div>
</template>

<script>
import {NetworkController} from "../../libs/NetworkController";

export default {
	name: "adminSettings",
	data: function () {
		return {
			CAC : false,
			CACMode: true,
			minTemp: '16',
			maxTemp: '30',
			defaultTemp: '24',
			defaultFanSpeed: '1',
		}
	},
	methods: {
		handleBeforeSetCAC() {
			return new Promise((resolve) => {
				if (this.$store.state.CAC === true) {
					this.$Modal.confirm({
						title: '关机',
						content: '您确认要关闭中央空调吗？',
						onOk: () => {
							this.$store.commit('setCAC', {toPower: false});
							resolve();
						}
					});
				} else {
					this.$Modal.confirm({
						title: '开机',
						content: '您确认要开启中央空调吗？',
						onOk: () => {
							this.$store.commit('setCAC', {toPower: true});
							resolve();
						}
					});
				}
			});
		},
		/**
		 * 开启或关闭中央空调
		 * @returns {Promise<void>}
		 */
		async handleSetCAC() {
			let nc = NetworkController.getInstance();
			if (this.$store.state.CAC === true) {
				await nc.setServerPower(true);
				await nc.setCACMode((this.CACMode === true ? 1 : -1), this.maxTemp, this.minTemp, this.defaultTemp, this.defaultFanSpeed, 1.5, 1.0, 0.5);
				await nc.setCACPower(true);
			} else {
				await nc.setCACPower(false);
			}
		},
		/**
		 * 管理员登出
		 * @returns {Promise<void>}
		 */
		async adminLogout() {
			this.$store.commit('setUsername', {username: ''});
		},
	}
}
</script>

<style scoped src="../../styles/settings.css"></style>
<style scoped>


</style>