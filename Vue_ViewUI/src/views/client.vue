<style scoped lang="less">
.index {
  width: 100%;
  //position: absolute;
  //top: 0;
  //bottom: 0;
  //left: 0;
  text-align: center;
  font-size: x-large;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;

  h1 {
    height: 150px;

    img {
      height: 100%;
    }
  }

  h2 {
    color: #666;
    margin-top: 25px;
    margin-bottom: 25px;

    p {
      margin: 0 0 20px;
    }
  }

  .ivu-row-flex {
    height: 100%;
  }

  .CtrlPanel {
    margin-top: 10%;
    margin-bottom: 10%;
    //font-size: xx-large;
  }

  .CardTitle {
    font-size: xx-large;
  }

  .CtrlGroup {
    margin-top: 2%;
    margin-bottom: 2%;
  }

}
</style>
<template>
  <div class="index">
    <Row type="flex" justify="center" align="middle">
      <Col span="12">
        <Card class="CtrlPanel">
          <h1 slot="title">
            <img src="../images/logo.png">
          </h1>
          <h2 class="CardTitle" slot="title">空调状态</h2>
          <h2 slot="extra"></h2>
          <h2>
            当前温度:{{ curnTemp }}<br>
            <br>
            当前风速:{{ curnWind }}<br>
            <br>
            当前模式:{{ curnMode }}<br>
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
    </Row>
  </div>
</template>
<script>
export default {
  data: function () {
    return {
      curnTemp: 26,
      curnWind: 3,
      curnMode: '致冷',
      buttonType: 'primary',
      acSwitch: false,
      acDisabled: true
    }
  },
  methods: {
    //空调的总控开关
    handleSwitch(status) {
      this.acDisabled = !status;
    },
    //空调温度控制，turnUp为升高的温度值，取值+1、-1
    changeTemp: function (event, turnUp) {
      this.curnTemp += turnUp;

      //下面是用于修复按钮点击后不失焦bug的代码：
      let target = event.target;
      if (target.nodeName === "SPAN") {
        target = event.target.parentNode;
      }
      target.blur();
      //可以忽略。
    },
    //空调风速控制，turnUp为升高的风速档位，取值+1、-1
    changeWind: function (event, turnUp) {
      this.curnWind += turnUp;

      //下面是用于修复按钮点击后不失焦bug的代码：
      let target = event.target;
      if (target.nodeName === "SPAN") {
        target = event.target.parentNode;
      }
      target.blur();
      //可以忽略。
    },
    //空调模式控制，toMode为目标模式，取值 致冷、制热
    changeMode: function (event, toMode) {
      this.curnMode = toMode;

      //下面是用于修复按钮点击后不失焦bug的代码：
      let target = event.target;
      if (target.nodeName === "SPAN") {
        target = event.target.parentNode;
      }
      target.blur();
      //可以忽略。
    }

  }
}
</script>
