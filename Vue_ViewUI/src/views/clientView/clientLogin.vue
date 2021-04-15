<template>
  <div>
    <Row type="flex" justify="center" align="middle">
      <Col :xs="20" :sm="18" :md="15" :lg="13" :xl="10">
        <Card class="CtrlPanel">
          <h1 class="titleHeader" slot="title">用户登录</h1>
          <Input class="CtrlGroup" v-model="roomId" size="large" clearable placeholder="请输入房间号"
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
import {checkin_u} from '../../connect_token.vue';
import {send_checkin_u} from '../../connect.vue';

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
      // this.checkIntegrity();
      this.$store.commit('setRoomId', 233);
      console.log(this.$store.state.roomId)

      /**
       * 测试：向全局存储存入一个键值对 uid123:'456username'
       */
      const testData = {
        key: 'uid123',
        value: '456username'
      };
      this.$store.commit('addSessionData',testData);
      console.log(this.$store.state.sessionData.uid123);//输出456username



      checkin_u(this.roomId, this.userPassword);
      this.$router.push({path: '/client'});
    },
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