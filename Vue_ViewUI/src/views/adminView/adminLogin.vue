<template>
  <div class="loginDiv">
    <Row type="flex" justify="center" align="middle">
      <Col :xs="22" :sm="18" :md="15" :lg="13" :xl="10" :xxl="8">
        <Card class="CtrlPanel">
          <h1 class="titleHeader" slot="title">管理员登录</h1>
          <Input class="CtrlGroup" v-model="username" size="large" clearable @on-enter="userLogin($event)"
                 placeholder="请输入用户名"></Input>
          <br>
          <Input class="CtrlGroup" v-model="password" size="large" type="password" password
                 @on-enter="userLogin($event)" placeholder="请输入密码"/>
          <br>
          <Button class="CtrlGroup" size="large" type="primary" shape="circle" @click="userLogin($event)">登录</Button>
        </Card>
      </Col>
    </Row>

  </div>

</template>

<script>
import {login_a} from '../../connect_token.vue';
import Vue from "vue";

export default {
  name: "adminLogin",
  data: function () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    userLogin(event) {
      login_a(this.username, this.password);
      this.$router.push({path: '/admin/main'});
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