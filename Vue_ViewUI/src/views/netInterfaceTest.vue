<template>
  <div>
<!--    这里是添加按钮区域，复制一行<Button>然后把@click的内容改成下面methods里的方法即可，$event原样传入-->
    <Button size="large" type="primary" shape="circle" @click="adminLogin($event)">adminLogin</Button>
    <Button size="large" type="primary" shape="circle" @click="createReport($event)">createReport</Button>


  </div>
</template>

<script>
import {login_a} from "../connect_token";
import {createreport_a} from "../connect_token";
import {createwaterbills_a} from "../connect_token";
import {turnonoff_a} from "../connect_token";
import {settemp_a} from "../connect_token";
import {setpattern_a} from "../connect_token";
import {setmode_a} from "../connect_token";
import {discount_a} from "../connect_token";
import {centerturnonoff_a} from "../connect_token";
import {signin_r} from "../connect_token";
import {logout_r} from "../connect_token";

export default {
  name: "netInterfaceTest",
  methods: {
    /**
     * 以下是按钮点击时调用的方法，内层包裹的是网络部分的接口
     * @param event 忽略
     */
    adminLogin(event) {
      login_a('testOnly', '123456');
    },
    createReport(e) {
      /**
       * 手动传入对应的参数即可
       */
      createreport_a();
    },
    createBill(e){
      createwaterbills_a();
    },
    adminTurnOnOff(e){
      turnonoff_a();
    },
    adminSetTemp(e){
      settemp_a();
    },
    adminSetWind(e){
      setmode_a();
    },
    adminSetMode(e){
      setpattern_a();
    },
    adminSetDiscount(e){
      discount_a();
    },
    adminTurnAllOnOff(e){
      centerturnonoff_a();
    },
    receptionSignIn(e){
      signin_r();
    },
    receptionSignOut(e){
      logout_r();
    },



  }
}

</script>

<style scoped>

</style>