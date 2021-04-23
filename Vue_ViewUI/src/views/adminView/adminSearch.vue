<template>
  <div>
    <Breadcrumb :style="{margin: '16px  1%'}">
      <BreadcrumbItem>管理员</BreadcrumbItem>
      <BreadcrumbItem>房间查询</BreadcrumbItem>
    </Breadcrumb>
    <Card>
      <Row class="adminSearch">
        <Input v-model="searchText" size="large" search enter-button placeholder="请输入房间号..."
               autocomplete="on" @on-search="searchRoom($event,searchText)"/>
      </Row>

      <div class="searchResult" v-if="hasSearched">
        <!--        <span>查询结果</span>-->
        <Row>
          <Col :xs="24" :sm="12" :md="12" :lg="8" :xl="8" :xxl="6" v-for="item in this.resultRoom">
            <Card class="acCard">
              <Row slot="title">
                <Col class="acCardTitle" :span="20">
                  <h3 class="acCardTitleText">房间{{ item.rid }}</h3>
                </Col>
                <Col align="end" :span="4">
                  <Button icon="ios-information-circle-outline" shape="circle"></Button>
                </Col>
              </Row>
              <!--              <Poptip slot="extra" placement="right" width="200">-->
              <!--                <Button icon="ios-settings" shape="circle" style="{padding-bottom:5px}"></Button>-->
              <!--                <div slot="content">-->
              <!--                  <h3>开关机：-->
              <!--                    <Switch v-model="item.power" size="large" type="primary" shape="circle">-->
              <!--                      <span slot="open">ON</span>-->
              <!--                      <span slot="close">OFF</span>-->
              <!--                    </Switch>-->
              <!--                  </h3>-->
              <!--                  <h3>打印详单：-->
              <!--                    <Button icon="md-download" shape="circle"></Button>-->
              <!--                  </h3>-->
              <!--                </div>-->
              <!--              </Poptip>-->
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

            </Card>
          </Col>
        </Row>
      </div>
    </Card>
  </div>
</template>

<script>
import random_str from "view-design/src/utils/random_str";
import Vue from "vue";

export default {
  name: "adminSearch",
  data: function () {
    return {
      hasSearched: false,
      searchText: '',
      // resultRoom: Object.create(null),
      resultRoom: new Map(),
    }
  },
  methods: {
    addAC(e) {
      let acTmp = {'rid': random_str(), 'power': true, 'curnTemp': 24, 'curnWind': 3, 'curnMode': '致冷'};
      Vue.set(this.resultRoom, acTmp.rid, acTmp);
      console.log(this.resultRoom);
    },
    searchRoom(e, searchInput) {
      this.hasSearched = true;
      console.log(searchInput);
      for (let k of Object.keys(this.resultRoom)) {
        Vue.delete(this.resultRoom, k);
      }

      this.addAC(e);
      this.addAC(e);
      this.addAC(e);
      this.addAC(e);
      this.addAC(e);
      this.addAC(e);
      this.addAC(e);
    },

  },
}
</script>

<style scoped>
.adminSearch {
  alignment: center;
  max-width: 720px;
  margin: 2vh auto;
}

.acCard {
  margin: 0.8vh 0.8vw;
}

.acCardTitle {
  display: inline-block;
  overflow: hidden;
  width: 80%;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: middle;
  transition: width .2s ease .2s;
}


.acCardTitleText {
  padding-left: 0.8vh;
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
  margin: .5vh;
}

.searchResult{
  alignment: center;
  margin: 4vh auto 2vh;
}
</style>