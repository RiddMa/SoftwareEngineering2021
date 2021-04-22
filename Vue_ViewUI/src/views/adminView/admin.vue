<style scoped>
/*.layout-con {*/
/*  height: 100%;*/
/*  width: 100%;*/
/*}*/

/*.menu-item span {*/
/*  display: inline-block;*/
/*  overflow: hidden;*/
/*  width: 90px;*/
/*  text-overflow: ellipsis;*/
/*  white-space: nowrap;*/
/*  vertical-align: middle;*/
/*  transition: width .2s ease .2s;*/

/*}*/

/*.menu-item i {*/
/*  transform: translateX(0px);*/
/*  transition: font-size .2s ease, transform .2s ease;*/
/*  vertical-align: middle;*/
/*  white-space: nowrap;*/
/*  font-size: 18px;*/
/*}*/

/*.collapsed-menu span {*/
/*  width: 0px;*/
/*  transition: width .2s ease;*/
/*}*/

/*.collapsed-menu i {*/
/*  transform: translateX(0px);*/
/*  white-space: nowrap;*/
/*  transition: font-size .2s ease .2s, transform .2s ease .2s;*/
/*  vertical-align: middle;*/
/*  font-size: 24px;*/
/*}*/

/*.SiderText {*/
/*  font-size: large;*/
/*  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;*/
/*  margin-left: .3vw;*/
/*}*/

.adminHeader {
  position: fixed;
  width: 100vw;
  height: 60px;
  line-height: 60px;
  background: #fff;
  margin-top: 5px;
  padding: 0;
  z-index: 9999;
}

.adminHeaderContent{
  padding-left: 6vw;
  vertical-align: bottom;
  margin-bottom: -7px;
}

.adminMenu{
  padding-left: 5vw;
  height: 50px;
  line-height: 50px;
}
</style>
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
          <span class="SiderText">空调概览</span>
        </MenuItem>
        <MenuItem name="2" to="/admin/search">
          <Icon type="ios-search"></Icon>
          <span class="SiderText">房间查询</span>
        </MenuItem>
        <MenuItem name="3" to="/admin/settings">
          <Icon type="ios-settings"></Icon>
          <span class="SiderText">偏好设置</span>
        </MenuItem>
      </Menu>
    </Header>
    <Content :style="{padding:'0 5vw 0 5vw'}">
      <div :style="{padding: '65px'}"></div>
      <router-view></router-view>

    </Content>


  </div>


  <!--  <div class="layout">-->
  <!--    &lt;!&ndash;    <Layout :style="{minHeight: '100vh'}">&ndash;&gt;-->
  <!--    <Sider collapsible :style="{position: 'fixed', height: '100vh', left: 0, overflow: 'auto'}" :collapsed-width="60"-->
  <!--           v-model="isCollapsed">-->
  <!--      <Menu mode="horizontal" active-name="1-1" theme="light" :class="menuitemClasses">-->
  <!--        <MenuItem name="1-1" to="/admin/main">-->
  <!--          <Icon type="ios-apps"></Icon>-->
  <!--          <span class="SiderText">空调概览</span>-->
  <!--        </MenuItem>-->
  <!--        <MenuItem name="1-2" to="/admin/search">-->
  <!--          <Icon type="ios-search"></Icon>-->
  <!--          <span class="SiderText">房间查询</span>-->
  <!--        </MenuItem>-->
  <!--        <MenuItem name="1-3" to="/admin/settings">-->
  <!--          <Icon type="ios-settings"></Icon>-->
  <!--          <span class="SiderText">偏好设置</span>-->
  <!--        </MenuItem>-->
  <!--      </Menu>-->
  <!--    </Sider>-->
  <!--    <Layout style="margin-left: 200px">-->
  <!--      <Header class="adminHeader">-->
  <!--        <h2>酒店空调管理系统-->
  <!--          <Button type="primary" shape="circle" @click="addAC($event)">[测试用]添加空调</Button>-->
  <!--        </h2>-->
  <!--      </Header>-->
  <!--      <Content :style="{padding: '0 16px 16px'}">-->
  <!--        <router-view></router-view>-->

  <!--      </Content>-->
  <!--    </Layout>-->
  <!--    &lt;!&ndash;    </Layout>&ndash;&gt;-->
  <!--  </div>-->
</template>
<script>
import Vue from "vue";
import random_str from "view-design/src/utils/random_str";

export default {
  name: 'admin',
  data() {
    return {
      // headerHeight:document.getElementById("adminHeader").clientHeight +"px",
    };
  },
  // mounted() {
  //   this.getHeaderHeight()
  //   window.addEventListener('resize',this.getHeaderHeight);
  // },
  methods: {
    addAC(e) {
      let acTmp = {'rid': random_str(), 'curnTemp': 24, 'curnWind': 3, 'curnMode': '致冷'};
      Vue.set(this.$store.state.roomInfo, acTmp.rid, acTmp);
      console.log(this.$store.state.roomInfo);
    },
  },
  // destroyed() {
  //   window.removeEventListener('resize',this.getHeaderHeight);
  // }
}
</script>
