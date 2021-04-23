<template>
  <div>
    <Row type="flex" justify="center" align="middle">

      <Col :xs="22" :sm="18" :md="15" :lg="13" :xl="10" :xxl="8">
        <Card class="CtrlPanel">
          <h1 class="titleHeader" slot="title">用户刷卡</h1>
          <Input class="CtrlGroup" v-model="roomId" size="large" clearable placeholder="请输入房间号"></Input>
          <br>
          <Input class="CtrlGroup" v-model="userPassword" size="large" type="password" password placeholder="请输入密码"/>
          <br>
          <Button class="CtrlGroup" size="large" type="primary" shape="circle" @click="userLogin($event)">登录</Button>
        </Card>
      </Col>
    </Row>

  </div>

</template>

<script>
import {checkin_u} from '../../connect_token.vue';
import Vue from "vue";

export default {
  name: "clientLogin",
  data: function () {
    return {
      roomId: '',
      userPassword: ''
    }
  },
  methods: {
    userLogin(event) {
      checkin_u(this.roomId, this.userPassword);
      Vue.set(this.$store.state.sessionData,'acSwitch',false);
      Vue.set(this.$store.state.sessionData,'curnTemp',26);
      Vue.set(this.$store.state.sessionData,'curnWind',3);
      Vue.set(this.$store.state.sessionData,'curnMode','致冷');
      this.$router.push({path: '/client'});
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
</style>