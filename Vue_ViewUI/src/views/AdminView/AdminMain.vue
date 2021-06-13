<template>
  <div>
    <Breadcrumb :style="{margin: '16px  1%'}">
      <BreadcrumbItem>管理员</BreadcrumbItem>
      <BreadcrumbItem>空调概览</BreadcrumbItem>
    </Breadcrumb>
    <Card>
      <div class="acList">
        <Row>
          <Col :xs="24" :sm="12" :md="12" :lg="8" :xl="6" :xxl="4" v-for="item in this.$store.state.roomInfo" v-bind:key="item.rid">
            <Card class="acCard">
              <Row slot="title">
                <Col class="acCardTitle" :span="20">
                  <h3 class="acCardTitleText">房间{{ item.rid }}</h3>
                </Col>
                <Col align="end" :span="4">
                  <Button icon="ios-information-circle-outline" shape="circle"></Button>
                </Col>
              </Row>

              <Row class="acCardContent">
                <Col :span="12">
                  <span>当前状态：</span>
                </Col>
                <Col align="middle" :span="12">
                  <Switch v-model="item.power" size="large" type="primary" shape="circle">
                    <span slot="open">ON</span>
                    <span slot="close">OFF</span>
                  </Switch>
                </Col>
              </Row>
              <div v-if="item.power" class="acStateInfo">
                <Row class="acCardContent">
                  <Col :span="12">
                    <span>当前温度：</span>
                  </Col>
                  <Col :span="12">
                    <Row>
                      <Col align="middle" :span="8">
                        <Button icon="ios-arrow-down" size="small" shape="circle"
                                @click="changeTemp($event,item.curnTemp,-1)"></Button>
                      </Col>
                      <Col align="middle" :span="8">
                        <span>{{ item.curnTemp }}</span>
                      </Col>
                      <Col align="middle" :span="8">
                        <Button icon="ios-arrow-up" size="small" shape="circle"></Button>
                      </Col>
                    </Row>
                  </Col>
                </Row>

                <Row class="acCardContent">
                  <Col :span="12">
                    <span>当前风速：</span>
                  </Col>
                  <Col :span="12">
                    <Row>
                      <Col align="middle" :span="8">
                        <Button icon="md-remove" size="small" shape="circle"></Button>
                      </Col>
                      <Col align="middle" :span="8">
                        <span>{{ item.curnWind }}</span>
                      </Col>
                      <Col align="middle" :span="8">
                        <Button icon="md-add" size="small" shape="circle"></Button>
                      </Col>
                    </Row>
                  </Col>
                </Row>

                <Row class="acCardContent">
                  <Col :span="12">
                    <span>当前模式：</span>
                  </Col>
                  <Col :span="12">
                    <Row>
                      <Col align="middle" :span="8">
                        <Button v-if="item.curnMode==='致冷'" size="small" type="primary" icon="ios-snow" shape="circle"
                                @click="changeMode($event,'致冷')"></Button>
                        <Button v-else icon="ios-snow" size="small" shape="circle"
                                @click="changeMode($event,'致冷')"></Button>
                      </Col>
                      <Col align="middle" :span="8">
                        <span>{{ item.curnMode }}</span>
                      </Col>
                      <Col align="middle" :span="8">
                        <Button v-if="item.curnMode==='制热'" size="small" type="primary" icon="ios-sunny" shape="circle"
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
          </Col>
        </Row>
      </div>
    </Card>
  </div>
</template>

<script>
export default {
  name: "adminMain",
  data: function () {
    return {}
  },
  methods: {
    popSettings(e, rid) {

    },
    changeTemp: function (e, turnUp) {

    },
    changeMode: function (e, toMode) {

    },
  }
}
</script>

<style scoped>
.acCardExtra {
  position: absolute;
  right: 0px;
  top: 0px;
}

.acCard {
  margin: 0.8vh 0.8vw;
}


.acCardTitle {

}

.acCardTitleText {
  padding-left: 0.8vw;
  padding-top: 2%;
  /*display: inline-block;*/
  overflow: hidden;
  width: 100%;
  height: auto;
  line-height: 20px;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: middle;
}

.acCardContent {
  margin-bottom: .75vh;
  margin-left: .75vw;
  margin-right: .75vw;
}

.acStateInfo {
  height: 80px;
}

</style>