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
import {checkin_u} from '../../connect_token.vue';
import {send_checkin_u} from '../../connect.vue';

export default {
  name: "clientLogin",
  data: function () {
    return {
      userName: '',
      userPassword: ''
    }
  },
  methods: {
    userLogin(event) {
      // this.checkIntegrity();
      this.$store.commit('setRoomId', 233);
      console.log(this.$store.state.roomId);
      send_checkin_u(this.userName, this.userPassword)
          .then(response => {
            console.log(response.data);
            let error_code;
            error_code= 0;
            let data;
            data = {
              uid: response.data.uid,
              username: response.data.username,
              token: response.data.token
            };
            console.log(data);
          })
          .catch(error => {
            console.log(error);
          });

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