<template>
  <div class="layout">
    <Header class="adminHeader">
      <h2 class="adminHeaderContent">
        酒店空调管理系统
        <Button type="primary" shape="circle" @click="addAC($event)">[测试用]添加空调</Button>
      </h2>
      <Menu class="adminMenu" mode="horizontal" active-name="1">
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

export default {
  name: 'admin',
  data() {
    return {
      activeTab: '1',
    };
  },
  methods: {
    addAC(e) {
      let acTmp = {'rid': random_str(), 'power': true, 'curnTemp': 24, 'curnWind': 3, 'curnMode': '致冷'};
      Vue.set(this.$store.state.roomInfo, acTmp.rid, acTmp);
      console.log(this.$store.state.roomInfo);
    },
  },
}
</script>

<style scoped>
.adminHeader {
  position: fixed;
  width: 100vw;
  height: 60px;
  line-height: 60px;
  background: #fff;
  padding: 5px 0 0 0;
  z-index: 9999;
}

.adminHeaderContent {
  padding-left: 6vw;
  vertical-align: bottom;
  margin-bottom: -7px;
}

.adminMenu {
  padding-left: 5vw;
  height: 50px;
  line-height: 50px;
}
</style>
