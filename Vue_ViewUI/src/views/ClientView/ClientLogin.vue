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
import random_str from "view-design/src/utils/random_str";

export default {
  name: "ClientLogin",
  data: function () {
    return {
      roomId: '',
      userPassword: ''
    }
  },
  methods: {
    /**
     * 向Vuex注册空调
     */
    addAC() {
      let acInfo = {'rid': random_str(), 'power': true, 'curnTemp': 24, 'curnWind': 3, 'curnMode': '致冷'};
      Vue.set(this.$store.state.roomInfo, acInfo.rid, acInfo);
      console.log(this.$store.state);
    },
    /**
     * 向Vuex注册用户
     * @param roomId
     */
    addUser(roomId) {

    },
    /**
     * 用户登录
     * @param event
     */
    userLogin(event) {
      if (checkin_u(this.roomId, this.userPassword)) {
        this.addUser(this.roomId);
        this.addAC();
      } else {
        //TODO:login failed
      }
      console.log(this.$store.state);
      this.$router.push({path: '/client'});// route to client view
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