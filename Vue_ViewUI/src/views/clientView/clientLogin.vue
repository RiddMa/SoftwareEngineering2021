<template>
  <div>
    <Row type="flex" justify="center" align="middle">
      <Col :xs="20" :sm="18" :md="15" :lg="13" :xl="10">
        <Card class="CtrlPanel">
          <h1 class="titleHeader" slot="title">用户登录</h1>
          <Input class="CtrlGroup" v-model="userName" size="large" clearable placeholder="请输入用户名"
                 style="width: 25vw"></Input>
          <br>
          <Input class="CtrlGroup" v-model="userPassword" size="large" type="password" password placeholder="请输入密码"
                 style="width: 25vw"/>
          <br>
          <Button class="CtrlGroup" size="large" type="primary" shape="circle" @click="userLogin($event)">登录</Button>
        </Card>
      </Col>
    </Row>

  </div>

</template>

<script>
import {client_login} from '../connect.vue';

export default {
  name: "clientLogin",
  data: function () {
    return {
      userName: '',
      userPassword: ''
    }
  },
  methods: {
    userLogin(e) {
      //
      // this.checkIntegrity();
      console.log(client_login(this.userName, this.userPassword));
      this.$router.push({path: '/client'});
    }
  }

}
</script>

<style scoped>
.CtrlPanel {
  margin-top: 25vh;
  margin-bottom: 25vh;
  text-align: center;
}

.CtrlGroup {
  margin-top: 2vh;
  margin-bottom: 2vh;
  font-size: large;
}

.titleHeader {
  margin-top: 2vh;
  margin-bottom: 2vh;
}
</style>