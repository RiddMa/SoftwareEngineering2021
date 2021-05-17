<template>
  <div class="index">
    <Row type="flex" justify="center" align="middle">
      <Col :xs="20" :sm="18" :md="15" :lg="13" :xl="10">
        <Card class="CtrlPanel">
          <h1 class="CardTitle" slot="title">
            <img src="../../images/logo.png">
          </h1>
          <h2 class="CardTitle" slot="title">空调状态</h2>
          <!--          <h2 slot="extra"></h2>-->
          <!--          <h2>-->
          <!--            &lt;!&ndash;            <iframe height="700" src="https://www.yunyoujun.cn/air-conditioner/"></iframe>&ndash;&gt;-->
          <!--            <p><span>当前温度:</span><span class="digitFont">{{ curnTemp }}</span></p>-->
          <!--            <p><span>当前风速:</span><span class="digitFont">{{ curnWind }}</span></p>-->
          <!--            <p>当前模式:{{ curnMode }}<br></p>-->
          <!--          </h2>-->

          <Row class="acCardContent">
            <Col :span="12">
              <span class="acCardContentText">当前状态：</span>
            </Col>
            <Col align="middle" :span="12" class="acCardContentText">
              <Switch v-model="thisRoom.power" size="large" type="primary" shape="circle">
                <span slot="open">ON</span>
                <span slot="close">OFF</span>
              </Switch>
            </Col>
          </Row>
          <div v-if="thisRoom.power" class="acStateInfo">
            <Row class="acCardContent">
              <Col :span="12">
                <span class="acCardContentText">当前温度：</span>
              </Col>
              <Col :span="12">
                <Row>
                  <Col align="middle" :span="8" class="acCardContentText">
                    <Button icon="ios-arrow-down" size="small" shape="circle"
                            @click="changeTemp($event,-1)"></Button>
                  </Col>
                  <Col align="middle" :span="8">
                    <span class="digitFont">{{ thisRoom.curnTemp }}</span>
                  </Col>
                  <Col align="middle" :span="8">
                    <Button icon="ios-arrow-up" size="small" shape="circle" class="acCardContentText"
                            @click="changeTemp($event,1)"></Button>
                  </Col>
                </Row>
              </Col>
            </Row>

            <Row class="acCardContent">
              <Col :span="12">
                <span class="acCardContentText">当前风速：</span>
              </Col>
              <Col :span="12" class="acCardContentText">
                <Row>
                  <Col align="middle" :span="8">
                    <Button icon="md-remove" size="small" shape="circle"
                            @click="changeWind($event,-1)"></Button>
                  </Col>
                  <Col align="middle" :span="8">
                    <span class="digitFont">{{ thisRoom.curnWind }}</span>
                  </Col>
                  <Col align="middle" :span="8">
                    <Button icon="md-add" size="small" shape="circle"
                            @click="changeWind($event,1)"></Button>
                  </Col>
                </Row>
              </Col>
            </Row>

            <Row class="acCardContent">
              <Col :span="12" class="acCardContentText">
                <span>当前模式：</span>
              </Col>
              <Col :span="12" class="acCardContentText">
                <Row>
                  <Col align="middle" :span="8">
                    <Button v-if="thisRoom.curnMode==='致冷'" size="small" type="primary" icon="ios-snow" shape="circle"
                            @click="changeMode($event,'致冷')"></Button>
                    <Button v-else icon="ios-snow" size="small" shape="circle"
                            @click="changeMode($event,'致冷')"></Button>
                  </Col>
                  <Col align="middle" :span="8">
                    <span>{{ thisRoom.curnMode }}</span>
                  </Col>
                  <Col align="middle" :span="8">
                    <Button v-if="thisRoom.curnMode==='制热'" size="small" type="primary" icon="ios-sunny" shape="circle"
                            @click="changeMode($event,'制热')"></Button>
                    <Button v-else icon="ios-sunny" size="small" shape="circle"
                            @click="changeMode($event,'制热')"></Button>
                  </Col>
                </Row>
              </Col>
            </Row>
          </div>
          <div v-else class="acStateInfo"></div>


        </Card>

<!--        <Card class="CtrlPanel">-->
<!--          <h2 class="CardTitle" slot="title">控制面板</h2>-->
<!--          <Switch class="CardTitle" slot="title" size="large" v-model="acSwitch" @on-change="handleSwitch">-->
<!--            <span slot="open">ON</span>-->
<!--            <span slot="close">OFF</span>-->
<!--          </Switch>-->
<!--          <h3>-->
<!--            <ButtonGroup class="CtrlGroup" size="large" shape="circle">-->
<!--              <Button type="primary" :disabled="acDisabled" @click="changeTemp($event,-1)">-->
<!--                <Icon type="ios-arrow-down"></Icon>-->
<!--                温度减-->
<!--              </Button>-->
<!--              <Button type="primary" :disabled="acDisabled" @click="changeTemp($event,1)">-->
<!--                温度加-->
<!--                <Icon type="ios-arrow-up"></Icon>-->
<!--              </Button>-->
<!--            </ButtonGroup>-->
<!--            <br>-->
<!--            <ButtonGroup class="CtrlGroup" size="large" shape="circle">-->
<!--              <Button type="primary" :disabled="acDisabled" @click="changeWind($event,-1)">-->
<!--                <Icon type="md-remove"></Icon>-->
<!--                风速减-->
<!--              </Button>-->
<!--              <Button type="primary" :disabled="acDisabled" @click="changeWind($event,1)">-->
<!--                风速加-->
<!--                <Icon type="md-add"></Icon>-->
<!--              </Button>-->
<!--            </ButtonGroup>-->
<!--            <br>-->
<!--            <ButtonGroup class="CtrlGroup" size="large" shape="circle">-->
<!--              <Button type="primary" :disabled="acDisabled" @click="changeMode($event,'致冷')">-->
<!--                <Icon type="ios-snow"></Icon>-->
<!--                致冷-->
<!--              </Button>-->
<!--              <Button type="primary" :disabled="acDisabled" @click="changeMode($event,'制热')">-->
<!--                制热-->
<!--                <Icon type="ios-sunny"></Icon>-->
<!--              </Button>-->
<!--            </ButtonGroup>-->
<!--          </h3>-->
<!--        </Card>-->
      </Col>
      <col flex="auto"></col>
    </Row>
  </div>
</template>
<script>
import {turnonoff_u} from '../../connect_token.vue';
import {settemp_u} from '../../connect_token.vue';
import {setmode_u} from '../../connect_token.vue';
import {showcast_u} from '../../connect_token.vue';
import Vue from "vue";

export default {
  name: 'client',
  data: function () {
    return {
      curnTemp: 24,
      curnWind: 3,
      curnMode: '致冷',
      buttonType: 'primary',
      acSwitch: false,
      acDisabled: true,
      title: null,
      thisRoom: this.$store.state.roomInfo[Object.keys(this.$store.state.roomInfo)[0]],
    }
  },
  methods: {
    //空调的总控开关
    handleSwitch(status) {
      this.acDisabled = !status;
      //TODO:传入用户名
      if (status === true) {
        console.log(turnonoff_u('testOnly', 1));
      } else {
        console.log(turnonoff_u('testOnly', 0));
      }
    },
    //空调温度控制，turnUp为升高的温度值，取值+1、-1
    changeTemp: function (event, turnUp) {
      this.thisRoom.curnTemp += turnUp;
      //TODO:传入用户名
      console.log(settemp_u('testOnly', this.curnTemp));
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
      this.thisRoom.curnWind += turnUp;
      //TODO:用户名和传入风速
      console.log(setmode_u('testOnly', 'H'));
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
      this.thisRoom.curnMode = toMode;
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

<style scoped src="../../styles/client.css"></style>
<style scoped lang="less">
.index {
  width: 100%;
  margin-top: 5vh;
  margin-bottom: 5vh;
  //text-align: center;
  font-size: x-large;

  h1 {
    height: 100px;
  }

  h2 {
    text-align: center;
    margin-top: 1vh;
    margin-bottom: 1vh;

    p {
      margin: 0 0 1vh;
    }
  }

  .ivu-row-flex {
    height: 100%;
  }
}

.CtrlPanel {
  margin-top: 5vh;
  margin-bottom: 5vh;
  //font-size: xx-large;
}

.CardTitle {
  font-size: xx-large;
}

.CardTitle img {
  max-width: 100%;
  max-height: 100%;
  display: block;
  margin: auto;
}

.CtrlGroup {
  margin-top: 1vh;
  margin-bottom: 1vh;
}

.digitFont {
  font-family: Digital7-mono;
  font-size: x-large;
  vertical-align: middle;
}
</style>