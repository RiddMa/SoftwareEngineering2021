<template>
  <div class="index">
    <Row type="flex" justify="center" align="middle">
      <Col :xs="20" :sm="18" :md="15" :lg="13" :xl="10">
        <Card class="CtrlPanel">
          <h1 class="CardTitle" slot="title">
            <img src="../../images/logo.png">
          </h1>
          <h2 class="CardTitle" slot="title">空调状态</h2>

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
                    <Button icon="ios-arrow-down" size="large" shape="circle"
                            @click="changeTemp($event,-1)"></Button>
                  </Col>
                  <Col align="middle" :span="8">
                    <span class="digitFont">{{ this.thisRoom.curnTemp }}</span>
                  </Col>
                  <Col align="middle" :span="8">
                    <Button icon="ios-arrow-up" size="large" shape="circle" class="acCardContentText"
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
                    <Button icon="md-remove" size="large" shape="circle"
                            @click="changeWind($event,-1)"></Button>
                  </Col>
                  <Col align="middle" :span="8">
                    <span class="digitFont">{{ this.thisRoom.curnWind }}</span>
                  </Col>
                  <Col align="middle" :span="8">
                    <Button icon="md-add" size="large" shape="circle"
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
                    <Button v-if="thisRoom.curnMode==='致冷'" size="large" type="primary" icon="ios-snow" shape="circle"
                            @click="changeMode($event,'致冷')"></Button>
                    <Button v-else icon="ios-snow" size="large" shape="circle"
                            @click="changeMode($event,'致冷')"></Button>
                  </Col>
                  <Col align="middle" :span="8">
                    <span style="vertical-align: middle">{{ thisRoom.curnMode }}</span>
                  </Col>
                  <Col align="middle" :span="8">
                    <Button v-if="thisRoom.curnMode==='制热'" size="large" type="primary" icon="ios-sunny" shape="circle"
                            @click="changeMode($event,'制热')"></Button>
                    <Button v-else icon="ios-sunny" size="large" shape="circle"
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
import util from "../../libs/util";

export default {
  name: 'Client',
  data: function () {
    return {
      title: null,
      thisRoom: this.$store.state.roomInfo[Object.keys(this.$store.state.roomInfo)[0]],
    }
  },
  methods: {
    /**
     * 空调温度控制
     * @param event
     * @param status
     */
    handleSwitch: function (event, status) {
      this.acDisabled = !status;
      //TODO:传入用户名
      if (status === true) {
        console.log(turnonoff_u('testOnly', 1));
      } else {
        console.log(turnonoff_u('testOnly', 0));
      }
    },
    /**
     * 空调温度控制
     * @param event
     * @param turnUp 升高的温度值，取值+1、-1
     */
    changeTemp: function (event, turnUp) {
      let targetTemp = this.thisRoom.curnTemp + turnUp;
      if (util.validateTemp(targetTemp) === true) {
        this.thisRoom.curnTemp = targetTemp;
        //TODO:传入用户名
        // settemp_u('testOnly', this.thisRoom.curnTemp);
      } else {
        //no-op
      }
      console.log(this.thisRoom.curnTemp);
    },
    /**
     * 空调风速控制
     * @param event
     * @param turnUp 升高的风速档位，取值+1、-1
     */
    changeWind: function (event, turnUp) {
      let targetWind = this.thisRoom.curnWind + turnUp;
      if (util.validateWind(targetWind) === true) {
        this.thisRoom.curnWind = targetWind;
        //TODO:用户名和传入风速
        console.log(setmode_u('testOnly', 'H'));
      } else {
        //no-op
      }
      console.log(this.thisRoom.curnWind);

    },
    /**
     * 空调模式控制
     * @param event
     * @param toMode 目标模式，取值 致冷、制热
     */
    changeMode: function (event, toMode) {
      this.thisRoom.curnMode = toMode;
      //TODO:目前还没有这个功能
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
  font-size: xx-large;
  vertical-align: middle;
}
</style>