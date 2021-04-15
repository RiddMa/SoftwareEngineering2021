<style scoped lang="less">
.index {
  width: 100%;
  margin-top: 5vh;
  margin-bottom: 5vh;
  text-align: center;
  font-size: x-large;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;

  h1 {
    height: 100px;

    img {
      height: 100%;
    }
  }

  h2 {
    margin-top: 1vh;
    margin-bottom: 1vh;

    p {
      margin: 0 0 1vh;
    }
  }

  .ivu-row-flex {
    height: 100%;
  }

  .CtrlPanel {
    margin-top: 5vh;
    margin-bottom: 5vh;
    //font-size: xx-large;
  }

  .CardTitle {
    font-size: xx-large;
  }

  .CtrlGroup {
    margin-top: 1vh;
    margin-bottom: 1vh;
  }

}
</style>
<template>
  <div class="index">
    <Row type="flex" justify="center" align="middle">
      <Col :xs="20" :sm="18" :md="15" :lg="13" :xl="10">
        <Card class="CtrlPanel">
          <h1 slot="title">
            <img src="../../images/logo.png">
          </h1>
          <h2 class="CardTitle" slot="title">空调状态</h2>
          <h2 slot="extra"></h2>
          <h2>
            <p>当前温度:{{ curnTemp }}<br></p>
            <p>当前风速:{{ curnWind }}<br></p>
            <p>当前模式:{{ curnMode }}<br></p>
          </h2>
        </Card>

        <!--          <Button @click="handleStart">Start View UI</Button>-->
        <Card class="CtrlPanel">
          <h2 class="CardTitle" slot="title">控制面板</h2>
          <Switch class="CardTitle" slot="title" size="large" v-model="acSwitch" @on-change="handleSwitch">
            <span slot="open">ON</span>
            <span slot="close">OFF</span>
          </Switch>
          <h3>
            <ButtonGroup class="CtrlGroup" size="large" shape="circle">
              <Button type="primary" :disabled="acDisabled" @click="changeTemp($event,-1)">
                <Icon type="ios-arrow-down"></Icon>
                温度减
              </Button>
              <Button type="primary" :disabled="acDisabled" @click="changeTemp($event,1)">
                温度加
                <Icon type="ios-arrow-up"></Icon>
              </Button>
            </ButtonGroup>
            <br>
            <ButtonGroup class="CtrlGroup" size="large" shape="circle">
              <Button type="primary" :disabled="acDisabled" @click="changeWind($event,-1)">
                <Icon type="md-remove"></Icon>
                风速减
              </Button>
              <Button type="primary" :disabled="acDisabled" @click="changeWind($event,1)">
                风速加
                <Icon type="md-add"></Icon>
              </Button>
            </ButtonGroup>
            <br>
            <ButtonGroup class="CtrlGroup" size="large" shape="circle">
              <Button type="primary" :disabled="acDisabled" @click="changeMode($event,'致冷')">
                <Icon type="ios-snow"></Icon>
                致冷
              </Button>
              <Button type="primary" :disabled="acDisabled" @click="changeMode($event,'制热')">
                制热
                <Icon type="ios-sunny"></Icon>
              </Button>
            </ButtonGroup>
          </h3>
        </Card>
      </Col>
      <col flex="auto"></col>
    </Row>
  </div>
</template>
<script>
import {turnonoff_u} from '../../connect.vue';
import {settemp_u} from '../../connect.vue';
import {setmode_u} from '../../connect.vue';
import {showcast_u} from '../../connect.vue';

export default {
  name: 'client',
  data: function () {
    return {
      curnTemp: 26,
      curnWind: 3,
      curnMode: '致冷',
      buttonType: 'primary',
      acSwitch: false,
      acDisabled: true,
      title: null
    }
  },
  methods: {
    //空调的总控开关
    handleSwitch(status) {
      this.acDisabled = !status;
      //TODO:传入用户名
      if(status===true){
        console.log(turnonoff_u('testOnly',1));
      }else{
        console.log(turnonoff_u('testOnly',0));
      }
    },
    //空调温度控制，turnUp为升高的温度值，取值+1、-1
    changeTemp: function (event, turnUp) {
      this.curnTemp += turnUp;
      //TODO:传入用户名
      console.log(settemp_u('testOnly',this.curnTemp));
      //TODO:这段代码后期要尽量封装一下
      //下面是用于修复按钮点击后不失焦bug的代码：
      // let target = event.target;
      // if (target.nodeName === "SPAN") {
      //   target = event.target.parentNode;
      // }
      // target.blur();
      //可以忽略。
    },
    //空调风速控制，turnUp为升高的风速档位，取值+1、-1
    changeWind: function (event, turnUp) {
      this.curnWind += turnUp;
      //TODO:用户名和传入风速
      console.log(setmode_u('testOnly','H'));
      //下面是用于修复按钮点击后不失焦bug的代码：
      // let target = event.target;
      // if (target.nodeName === "SPAN") {
      //   target = event.target.parentNode;
      // }
      // target.blur();
      //可以忽略。
    },
    //空调模式控制，toMode为目标模式，取值 致冷、制热
    changeMode: function (event, toMode) {
      this.curnMode = toMode;
      //TODO:目前还没有这个功能
      //下面是用于修复按钮点击后不失焦bug的代码：
      // let target = event.target;
      // if (target.nodeName === "SPAN") {
      //   target = event.target.parentNode;
      // }
      // target.blur();
      //可以忽略。
    }

  }
}
</script>
