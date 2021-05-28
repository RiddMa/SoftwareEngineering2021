<template>
  <div class="layout">
    <Header class="aHeader">
      <h2 class="aHeaderContent">
        酒店空调管理系统
        <Button type="primary" shape="circle" @click="addAC(defaultAC)">[测试用]添加空调</Button>
      </h2>
      <Menu class="aMenu" mode="horizontal" active-name="1">
        <MenuItem name="1" to="/admin/main">
          <Icon type="ios-apps"></Icon>
          <span class="MenuText">空调概览</span>
        </MenuItem>
        <MenuItem name="2" to="/admin/search">
          <Icon type="ios-search"></Icon>
          <span class="MenuText">房间查询</span>
        </MenuItem>
        <MenuItem name="3" to="/admin/settings">
          <Icon type="ios-settings"></Icon>
          <span class="MenuText">偏好设置</span>
        </MenuItem>
      </Menu>
    </Header>
    <Content :style="{padding:'0 5vw 0 5vw'}">
      <div :style="{padding: '60px'}"></div>
      <keep-alive>
        <router-view></router-view>
      </keep-alive>
    </Content>
  </div>
</template>

<script>
import Vue from "vue";
import random_str from "view-design/src/utils/random_str";
import util from "../../libs/util";

export default {
  name: 'admin',
  data() {
    return {
      defaultAC: {'rid': random_str(), 'power': true, 'curnTemp': 24, 'curnWind': 3, 'curnMode': '致冷'},
      activeTab: '1',
    };
  },
  methods: {
    /**
     * 向 Vuex 注册空调
     * @param acInfo
     */
    addAC: function (acInfo) {
      Vue.set(this.$store.state.roomInfo, acInfo.rid, acInfo);
      console.log(this.$store.state);
    },
  },
}
</script>

<style scoped src="../../styles/header.css"></style>
<style scoped>

</style>
