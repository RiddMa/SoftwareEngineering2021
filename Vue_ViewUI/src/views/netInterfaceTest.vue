<template>
<div>
  <Button size="large" type="primary" shape="circle" @click="userLogin($event)">登录</Button>
  <Button size="large" type="primary" shape="circle" @click="userLogin($event)">登录</Button>


</div>
</template>

<script>
import {send_checkin_u} from "../connect_token";

export default {
  name: "netInterfaceTest",
  methods: {
    adminLogin(event) {
      send_checkin_u(this.userName, this.userPassword);
    },
  }
}
</script>

<style scoped>

</style>