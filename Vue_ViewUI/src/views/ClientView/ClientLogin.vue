<template>
  <div>
    <Row type="flex" justify="center" align="middle">

      <Col :xs="22" :sm="18" :md="15" :lg="13" :xl="10" :xxl="8">
        <Card class="CtrlPanel">
          <h1 class="titleHeader" slot="title">用户刷卡</h1>
          <Input class="CtrlGroup" v-model="roomId" size="large" clearable placeholder="请输入房间号"></Input>
          <br>
          <Input class="CtrlGroup" v-model="password" size="large" type="password" password placeholder="请输入密码"/>
          <br>
          <Button class="CtrlGroup" size="large" type="primary" shape="circle" @click="userLogin($event)">登录</Button>
        </Card>
      </Col>
    </Row>

  </div>

</template>

<script>
import {NetworkController} from "../../libs/NetworkController.js";
import Vue from "vue";
import random_str from "view-design/src/utils/random_str";

export default {
  name: "ClientLogin",
  data: function () {
    return {
      roomId: '',
      password: ''
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
    async userLogin(event) {
      let result = await NetworkController.getInstance().login(this.roomId, this.password, 0);
      if (result === 1) {
        this.addUser(this.roomId);
        this.addAC();
        this.$router.push({path: '/client'});// route to client view
      } else {
        //TODO:login failed
        this.addUser(this.roomId);
        this.addAC();
        this.$router.push({path: '/client'});// route to client view
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
</style>