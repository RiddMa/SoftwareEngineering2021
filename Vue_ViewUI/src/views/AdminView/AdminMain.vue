<template>
	<div>
		<Breadcrumb :style="{margin: '16px  1%'}">
			<BreadcrumbItem>管理员</BreadcrumbItem>
			<BreadcrumbItem>空调概览</BreadcrumbItem>
		</Breadcrumb>
		<Card>
			<div class="acList">
				<Row>
					<Col v-for="item in this.$store.state.roomInfo" v-bind:key="item.rid" :lg="8" :md="12" :sm="12" :xl="6"
					     :xs="24"
					     :xxl="4">
						<Card class="acCard">
							<Row slot="title">
								<Col :span="20" class="acCardTitle">
									<h3 class="acCardTitleText">房间{{ item.rid }}</h3>
								</Col>
								<Col :span="4" align="end">
									<Button icon="ios-information-circle-outline" shape="circle"></Button>
								</Col>
							</Row>

							<Row class="acCardContent">
								<Col :span="12">
									<span>当前状态：</span>
								</Col>
								<Col :span="12" align="middle">
									<Switch v-model="item.power" shape="circle" size="large" type="primary">
										<span slot="open">ON</span>
										<span slot="close">OFF</span>
									</Switch>
								</Col>
							</Row>
							<div v-if="item.power" class="acStateInfo">
								<Row class="acCardContent">
									<Col :span="12">
										<span>当前温度：</span>
									</Col>
									<Col :span="12">
										<Row>
											<Col :span="8" align="middle">
												<Button icon="ios-arrow-down" shape="circle" size="small"
												        @click="changeTemp($event,item.curnTemp,-1)"></Button>
											</Col>
											<Col :span="8" align="middle">
												<span>{{ item.curnTemp }}</span>
											</Col>
											<Col :span="8" align="middle">
												<Button icon="ios-arrow-up" shape="circle" size="small"></Button>
											</Col>
										</Row>
									</Col>
								</Row>

								<Row class="acCardContent">
									<Col :span="12">
										<span>当前风速：</span>
									</Col>
									<Col :span="12">
										<Row>
											<Col :span="8" align="middle">
												<Button icon="md-remove" shape="circle" size="small"></Button>
											</Col>
											<Col :span="8" align="middle">
												<span>{{ item.curnWind }}</span>
											</Col>
											<Col :span="8" align="middle">
												<Button icon="md-add" shape="circle" size="small"></Button>
											</Col>
										</Row>
									</Col>
								</Row>

								<Row class="acCardContent">
									<Col :span="12">
										<span>当前模式：</span>
									</Col>
									<Col :span="12">
										<Row>
											<Col :span="8" align="middle">
												<Button v-if="item.curnMode==='致冷'" icon="ios-snow" shape="circle" size="small" type="primary"
												        @click="changeMode($event,'致冷')"></Button>
												<Button v-else icon="ios-snow" shape="circle" size="small"
												        @click="changeMode($event,'致冷')"></Button>
											</Col>
											<Col :span="8" align="middle">
												<span>{{ item.curnMode }}</span>
											</Col>
											<Col :span="8" align="middle">
												<Button v-if="item.curnMode==='制热'" icon="ios-sunny" shape="circle" size="small" type="primary"
												        @click="changeMode($event,'制热')"></Button>
												<Button v-else icon="ios-sunny" shape="circle" size="small"
												        @click="changeMode($event,'制热')"></Button>
											</Col>
										</Row>
									</Col>
								</Row>
							</div>
							<div v-else class="acStateInfo"></div>


						</Card>
					</Col>
				</Row>
			</div>
		</Card>
	</div>
</template>

<script>
export default {
	name: "adminMain",
	data: function () {
		return {
			adminRoomState: this.$store.state.adminRoomState
		}
	},
	methods: {
		popSettings(e, rid) {

		},
		changeTemp: function (e, turnUp) {

		},
		changeMode: function (e, toMode) {

		},
	}
}
</script>

<style scoped>
.acCardExtra {
	position: absolute;
	right: 0px;
	top: 0px;
}

.acCard {
	margin: 0.8vh 0.8vw;
}


.acCardTitle {

}

.acCardTitleText {
	padding-left: 0.8vw;
	padding-top: 2%;
	/*display: inline-block;*/
	overflow: hidden;
	width: 100%;
	height: auto;
	line-height: 20px;
	text-overflow: ellipsis;
	white-space: nowrap;
	vertical-align: middle;
}

.acCardContent {
	margin-bottom: .75vh;
	margin-left: .75vw;
	margin-right: .75vw;
}

.acStateInfo {
	height: 80px;
}

</style>