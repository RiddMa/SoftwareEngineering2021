<template>
  <div>
<!--    这里是添加按钮区域，复制一行<Button>然后把@click的内容改成下面methods里的方法即可，$event原样传入-->
    <Button size="large" type="primary" shape="circle" @click="adminLogin($event)">adminLogin</Button>
    <Button size="large" type="primary" shape="circle" @click="createReport($event)">createReport</Button>
    <Button size="large" type="primary" shape="circle" @click="createBill($event)">createBill</Button>
    <Button size="large" type="primary" shape="circle" @click="adminTurnOnOff($event)">adminTurnOnOff</Button>
    <Button size="large" type="primary" shape="circle" @click="adminSetTemp($event)">adminSetTemp</Button>
    <Button size="large" type="primary" shape="circle" @click="adminSetMode($event)">adminSetMode</Button>
    <Button size="large" type="primary" shape="circle" @click="adminSetWind($event)">adminSetWind</Button>
    <Button size="large" type="primary" shape="circle" @click="adminSetDiscount($event)">adminSetDiscount</Button>
    <Button size="large" type="primary" shape="circle" @click="adminTurnAllOnOff($event)">adminTurnAllOnOff</Button>
    <Button size="large" type="primary" shape="circle" @click="receptionSignIn($event)">receptionSignIn</Button>
    <Button size="large" type="primary" shape="circle" @click="receptionSignOut($event)">receptionSignOut</Button>


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
      createreport_a('114514');
    },
    createBill(e){
      createwaterbills_a('114514');
    },
    adminTurnOnOff(e){
      turnonoff_a('103','1');
    },
    adminSetTemp(e){
      settemp_a('104','55');
    },
    adminSetWind(e){
      setmode_a('104','6');
    },
    adminSetMode(e){
      setpattern_a();
    },
    adminSetDiscount(e){
      discount_a('103','0.1');
    },
    adminTurnAllOnOff(e){
      centerturnonoff_a('0');
    },
    receptionSignIn(e){
      signin_r('10086');
    },
    receptionSignOut(e){
      logout_r('103');
    },



  }
}

</script>

<style scoped>

</style>