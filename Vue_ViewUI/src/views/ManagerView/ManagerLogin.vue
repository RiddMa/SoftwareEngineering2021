<template>
  <div class="loginDiv">
    <Row type="flex" justify="center" align="middle">
      <Col :xs="22" :sm="18" :md="15" :lg="13" :xl="10" :xxl="8">
        <Card class="CtrlPanel">
          <h1 class="titleHeader" slot="title">经理登录</h1>
          <Input class="CtrlGroup" v-model="username" size="large" clearable @on-enter="managerLogin"
                 placeholder="请输入账户名"></Input>
          <br>
          <Input class="CtrlGroup" v-model="password" size="large" type="password" password
                 @on-enter="managerLogin" placeholder="请输入密码"/>
          <br>
          <Button class="CtrlGroup" size="large" type="primary" shape="circle" @click="managerLogin">登录</Button>
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
  name: "ManagerLogin",
  data: function () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
	  async managerLogin(event) {
		  let nc = NetworkController.getInstance();
		  let errCode = await nc.login(this, this.username, this.password, 3);
		  if (errCode === 0) {
			  this.$store.commit('setUsername', {username: this.username});
			  this.$router.push({path: '/manager/daily'});
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