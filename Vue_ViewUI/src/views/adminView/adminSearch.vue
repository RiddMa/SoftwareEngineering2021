<template>
  <div class="tabBase">
    <Breadcrumb :style="{margin: '16px  1%'}">
      <BreadcrumbItem>管理员</BreadcrumbItem>
      <BreadcrumbItem>房间查询</BreadcrumbItem>
    </Breadcrumb>
    <Card>
      <Row class="searchBar">
        <Input v-model="searchText" size="large" search enter-button placeholder="请输入房间号..."
               autocomplete="on" @on-search="searchRoom($event,searchText)"/>
      </Row>

      <div class="searchResult" v-if="hasSearched">
        <Row>
          <Col :xs="24" :sm="12" :md="12" :lg="8" :xl="6" :xxl="4" v-for="item in this.resultRoom">
            <Card class="acCard">
              <Row slot="title">
                <Col class="acCardTitle" :span="20">
                  <h3 class="acCardTitleText">房间{{ item.rid }}</h3>
                </Col>
                <Col align="end" :span="4">
                  <Button icon="ios-information-circle-outline" shape="circle"
                          @click="printDetailedList($event,item.rid)"></Button>
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
              <Row class="acCardContent">
                <Col :span="12">
                  <span>累计金额：</span>
                </Col>
                <Col align="middle" :span="12">
                  <span><b>￥{{item.cost}}</b></span>
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
import random_str from "view-design/src/utils/random_str";
import Vue from "vue";

export default {
  name: "adminSearch",
  data: function () {
    return {
      hasSearched: false,
      searchText: '',
      resultRoom: Object.create(null),
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
    printDetailedList(e, rid) {
      //TODO
    },

  },
}
</script>

<style scoped src="../../styles/search.css"></style>
<style scoped>

</style>