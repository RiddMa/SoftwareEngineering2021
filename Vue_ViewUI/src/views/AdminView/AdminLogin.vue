<template>
	<div class="loginDiv">
		<Row align="middle" justify="center" type="flex">
			<Col :lg="13" :md="15" :sm="18" :xl="10" :xs="22" :xxl="8">
				<Card class="CtrlPanel">
					<h1 slot="title" class="titleHeader">管理员登录</h1>
					<Input v-model="username" class="CtrlGroup" clearable placeholder="请输入账户名" size="large"
					       @on-enter="adminLogin($event)"></Input>
					<br>
					<Input v-model="password" class="CtrlGroup" password placeholder="请输入密码" size="large"
					       type="password" @on-enter="adminLogin($event)"/>
					<br>
					<Button class="CtrlGroup" shape="circle" size="large" type="primary" @click="adminLogin($event)">登录</Button>
				</Card>
			</Col>
		</Row>

	</div>

</template>

<script>
import {login_a} from '../../connect_token.vue';
import Vue from "vue";
import {NetworkController} from "../../libs/NetworkController";

export default {
	name: "adminLogin",
	data: function () {
		return {
			username: '',
			password: ''
		}
	},
	methods: {
		async adminLogin(event) {
			let nc = NetworkController.getInstance();
			let errCode = await nc.login(this.username, this.password, 1);
			if (errCode === 0) {
				this.$store.commit('setUsername', {username: this.username});
				this.$router.push({path: '/admin/main'});
			} else if (errCode === 1) {
				//TODO:login failed
			} else if (errCode === -1) {
				//TODO:network error
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

.loginDiv {
	min-height: 90vh;
}
</style>