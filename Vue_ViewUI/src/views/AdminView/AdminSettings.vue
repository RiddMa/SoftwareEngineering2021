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
							<Switch slot="extra" v-model="this.$store.state.CACState" :before-change="handleBeforeChangeCAC"
							        shape="circle"
							        size="large" type="primary" @on-change="handleChangeCAC()">
								<span slot="open">ON</span>
								<span slot="close">OFF</span>
							</Switch>
						</Cell>
						<Cell class="settings" title="管理员登出">
							<Button slot="extra" shape="circle" type="error" @click="adminLogout($event,adminId)">登出</Button>
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
	methods: {
		handleBeforeChangeCAC() {
			return new Promise((resolve) => {
				if (this.$store.state.CACState === true) {
					this.$Modal.confirm({
						title: '关机',
						content: '您确认要关闭中央空调吗？',
						onOk: () => {
							this.$store.state.CACState = false;
							resolve();
						}
					});
				} else {
					this.$Modal.confirm({
						title: '开机',
						content: '您确认要开启中央空调吗？',
						onOk: () => {
							this.$store.state.CACState = true;
							resolve();
						}
					});
				}

			});
		},
		async handleChangeCAC() {
			let nc = NetworkController.getInstance();
			if (this.$store.state.CACState === false) {
				await nc.toggleServerPower(true);
				await nc.setCACMode(1, 30, 16, 26, '1', 1.5, 1.0, 0.5);
				await nc.toggleCACPower(true);
			}
		}
	}
}
</script>

<style scoped src="../../styles/settings.css"></style>
<style scoped>


</style>